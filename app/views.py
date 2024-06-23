from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Apropos, AvisClient, Tarif, Reservation, Bannier, Agence, Logo
from .process import html_to_pdf
from django.template.loader import get_template
from django.http import HttpResponse
from django.views import View
from xhtml2pdf import pisa 

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
        messages.success(request, "Votre reservation a été enregistré avec succes, cliquer sur le bouton ci-dessous pour télécharger voter billet")

        return redirect('download_pdf')

    # return render(request, "reservation.html", context)

    # Contact form 
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        send_mail('Un message de notre client', message, email, ['josiasfaustinboukan@gmail.com'])
        messages.success(request, 'Votre message a été envoyé avec succes')
        return  redirect("/home")


    return render(request, "app/base.html", context )

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

        my_model = Reservation(r_nom=r_nom,r_prenom=r_prenom,r_piece_nationale=r_piece_nationale,r_date=r_date,r_destination=r_destination,r_agences=r_agences,r_phone=r_phone,r_adresse=r_adresse,r_provenance=r_provenance)
        my_model.save()
        messages.success(request, "Votre reservation a été enregistré avec succes")

        return redirect('download_pdf')

    # return render(request, "reservation.html", context)

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
