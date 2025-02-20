from tokenize import generate_tokens
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Apropos, AvisClient, Tarif, Reservation, Bannier, Agence, Logo, Profile
from .process import html_to_pdf
from django.template.loader import get_template, render_to_string
from django.http import HttpResponse
from django.views import View
from xhtml2pdf import pisa 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail, EmailMessage
from app.tokens import account_activation_token
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    Apropos_details = Apropos.objects.all()
    clients = AvisClient.objects.all()
    trajets = Tarif.objects.all()
    bannier_images = Bannier.objects.all()
    agences = Agence.objects.all()
    logo_images = Logo.objects.all()

    context = {
        'company': Apropos_details,
        'avis': clients,
        'destinations': trajets,
        'banniers': bannier_images,
        'ville_agences':  agences,
        'logo_images': logo_images,
    }

    # Contact form 
    if request.method == 'POST':
        name = request.POST['nom']
        subject = request.POST['object']
        email = request.POST['mail']
        from_email = settings.EMAIL_HOST_USER
        message = request.POST['message']
        to_list = [email]

        send_mail(subject, message, from_email, to_list, fail_silently=True)
        messages.success(request, 'Votre message a été envoyé avec succes')
        return  redirect("/")

    return render(request, "app/home.html", context )

def signin(request):
    logo_images = Logo.objects.all()
    bannier_profile = Profile.objects.all()

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "app/profile.html", context={'fname': fname, 'logo_images': logo_images, 'profile_bannier': bannier_profile}) 
        else:
            messages.error(request, "nom d'utilisateur ou mot de passe incorrect")
            return redirect("signin")

    return render(request, "app/signin.html", context={'logo_images': logo_images, 'profile_bannier': bannier_profile} )

def signup(request):
    logo_images = Logo.objects.all()

    context = {
        'logo_images': logo_images,
    }

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        firstname = request.POST.get('fname')
        last_name = request.POST.get('lname')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if User.objects.filter(username=username):
            messages.error(request, "Ce nom d'utilisateur existe deja!")
            return redirect("signup")
        if User.objects.filter(email=email):
            messages.error(request, 'cette adresse mail existe deja!')
            return redirect("signup")
        if len(username) > 10:
            messages.error(request, "Ce nom d'utilisateur est trop long")
            return redirect("signup")
        if pass1 != pass2:
            messages.error(request, "Les mots de passe ne correspond pas")
            return redirect("signup")
        if not username.isalnum():
            messages.error(request, "le nom d'utilisateur doit etre en alpha-numerique")
            return redirect('signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = firstname
        myuser.last_name = last_name
        myuser.is_active = False
        myuser.save()

        messages.success(request, "Votre compte a été crée avec succes. \n Veuillez clicker sur le lien que nous vous avons envoyé par mail \n pour activer votre compte")

        #Email addresse confirmation
        current_site = get_current_site(request)
        mail_subject = "Activation du compte"
        message = render_to_string('account_activation.html',{
            "user": myuser, 
            "domain": current_site, 
            "uid": urlsafe_base64_encode(force_bytes(myuser.pk)),
            "token": account_activation_token.make_token(myuser)
            })
        
        mail = EmailMessage(mail_subject,message,settings.EMAIL_HOST_USER,[myuser.email],)
        mail.fail_silently = True
        mail.send()

        return redirect('signin')

    return render(request, "app/signup.html", context )

@login_required(login_url= 'signin')
def profile(request):
    logo_images = Logo.objects.all()
    bannier_profile = Profile.objects.all()

    context = {
        'logo_images': logo_images,
        'profile_bannier': bannier_profile,
    }

    # reservation 
    if request.method == 'POST':
        r_nom = request.POST['name'] 
        r_prenom = request.POST['prenom']  
        r_piece_nationale = request.POST['piece']
        r_date = request.POST['date'] 
        r_destination = request.POST['trajet']
        r_agences = request.POST['agence']
        r_phone = request.POST['phone'] 
        r_adresse = request.POST['adresse'] 
        r_provenance = request.POST['provenance']
        user_id = request.POST['user_id']

        my_model = Reservation(r_nom=r_nom,r_prenom=r_prenom,r_piece_nationale=r_piece_nationale,r_date=r_date,
        r_destination=r_destination,r_provenance=r_provenance,r_agences=r_agences,r_phone=r_phone,r_adresse=r_adresse,user_id=user_id)
        my_model.save()
        messages.success(request, "Reservation effectuée avec succes, cliquer le bouton ci-dessous pour télécharger voter billet")

        return redirect('download_pdf')
    return render(request, "app/profile.html", context ) 


@login_required(login_url= 'signin')
def dashboard(request):

    logo_images = Logo.objects.all()
    bannier_profile = Profile.objects.all()

    # if request.user.is_authenticated:
    #     user_id = request.user.id
    user_reservation = Reservation.objects.order_by('-create_date').filter(user_id = request.user.id)

    context = {
        'logo_images': logo_images,
        'profile_bannier': bannier_profile,
        'reservations': user_reservation,
    }

    return render(request, 'app/dashboard.html', context)

def signout(request):
    logout(request)
    messages.success(request, "Vous vous etes deconnecté")
    return redirect("home")

def activation(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    if myuser is not None and account_activation_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Votre compte a été activé avec succes")
        return redirect("/") 
    else:
        return render(request, "activation_faild.html")
    

def agences(request):
    Apropos_details = Apropos.objects.all()
    clients = AvisClient.objects.all()
    trajets = Tarif.objects.all()
    bannier_images = Bannier.objects.all()
    agences = Agence.objects.all()
    logo_images = Logo.objects.all()

    context = {
        'company': Apropos_details,
        'avis': clients,
        'destinations': trajets,
        'banniers': bannier_images,
        'ville_agences':  agences,
        'logo_images': logo_images,
    }


    return render(request, "app/agences.html", context )

def download_pdf(request):
    Apropos_details = Apropos.objects.all()
    clients = AvisClient.objects.all()
    trajets = Tarif.objects.all()
    bannier_images = Bannier.objects.all()
    agences = Agence.objects.all()
    logo_images = Logo.objects.all()

    context = {
        'company': Apropos_details,
        'avis': clients,
        'destinations': trajets,
        'banniers': bannier_images,
        'ville_agences':  agences,
        'logo_images': logo_images,
    }

    return render(request, "app/download_pdf.html", context )

def reservation_pdf(request):
    logo_images = Logo.objects.all()

    higher_id = Reservation.objects.all().values_list('id', flat=True).order_by('-id').first()  
    mydata = Reservation.objects.filter(id=higher_id).values()
    context =  {
        'reservation_data': mydata,
        'logo_images': logo_images,
    }

    return render(request, 'app/reservation_pdf.html', context)

#Creating a class based view
class GeneratePdf(View):
     def get(self, request, *args, **kwargs):
        higher_id = Reservation.objects.all().values_list('id', flat=True).order_by('-id').first()  
        mydata = Reservation.objects.filter(id=higher_id).values()
        context =  {
        'reservation_data': mydata,
        }
         
        # getting the template
        template = get_template('app/reservation_pdf.html')
        html = template.render(context)
        pdf = html_to_pdf('app/reservation_pdf.html', context)
         
         # rendering the template
        response =  HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="reservation.pdf"'

        # create pdf
        pisa_status = pisa.CreatePDF(
            html, dest= response)

        return response
