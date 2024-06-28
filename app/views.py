from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Apropos, AvisClient, Tarif, Reservation, Bannier, Agence, Logo, Profile
from .process import html_to_pdf
from django.template.loader import get_template
from django.http import HttpResponse
from django.views import View
from xhtml2pdf import pisa 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

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
    # if request.method == 'POST':
    #     name = request.POST['name']
    #     email = request.POST['email']
    #     message = request.POST['message']

    #     send_mail('Un message de notre client', message, email, ['josiasfaustinboukan@gmail.com'])
    #     messages.success(request, 'Votre message a été envoyé avec succes')
    #     return  redirect("/home")

    return render(request, "app/base.html", context )

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
            return render(request, "app/logout.html", context={'fname': fname, 'logo_images': logo_images, 'profile_bannier': bannier_profile}) 
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

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = firstname
        myuser.last_name = last_name
        myuser.save()

        messages.success(request, "Votre compte a été crée avec succes")
        return redirect('signin')

    return render(request, "app/signup.html", context )

def logout(request):
    logo_images = Logo.objects.all()
    bannier_profile = Profile.objects.all()

    context = {
        'logo_images': logo_images,
        'profile_bannier': bannier_profile,
    }

    #reservation 
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

        my_model = Reservation(r_nom=r_nom,r_prenom=r_prenom,r_piece_nationale=r_piece_nationale,r_date=r_date,r_destination=r_destination,r_provenance=r_provenance,r_agences=r_agences,r_phone=r_phone,r_adresse=r_adresse)
        my_model.save()
        messages.success(request, "Reservation effectuée avec succes, cliquer le bouton ci-dessous pour télécharger voter billet")

        return redirect('download_pdf')
    return render(request, "app/logout.html", context ) 

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

    return render(request, 'reservation_pdf.html', context)

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
