from io import BytesIO
from django.core.files import File
from django.db import models
import qrcode
from PIL import Image
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class Logo(models.Model):
    nom = models.CharField(max_length=70)
    image = models.ImageField()

    def __str__(self):
        return self.nom

class Bannier(models.Model):
    nom_bannier = models.CharField(max_length=200)
    sous_titre_bannier = models.CharField(max_length=200, null=True)
    titre_bannier = models.CharField(max_length=200, null=True)
    texte_bannier = models.CharField(max_length=400, null=True)
    image = models.ImageField()

    def __str__(self):
        return self.nom_bannier

class Reservation(models.Model):
    r_nom = models.CharField(max_length=200, null=True)
    r_prenom = models.CharField(max_length=200, null=True)
    r_piece_nationale = models.CharField(max_length=70, null=True)
    r_date = models.DateField(max_length=70, null=True)
    r_destination= models.CharField(max_length=200, null=True)
    r_provenance= models.CharField(max_length=200, null=True)
    r_agences = models.CharField(max_length=70, null=True)
    r_phone = models.CharField(max_length=70, null=True)
    r_adresse = models.CharField(max_length=200, null=True)
    qr_code = models.ImageField(blank=True, upload_to='code')
    payement = models.BooleanField(default=False)
    create_date = models.DateTimeField(blank=True, default=datetime.now)

    def __str__(self):
        return str(self.r_nom)
    
    def save(self, *args, **kwargs):
        qr_image = qrcode.make(self.r_nom)
        qr_offset = Image.new('RGB', (310, 310), 'white')
        qr_offset.paste(qr_image)
        files_name = f'{self.r_nom}-{self.id}qr.png'
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.qr_code.save(files_name, File(stream), save=False)
        qr_offset.close()
        super().save(*args, **kwargs)


class Apropos(models.Model):
    nom = models.CharField(max_length=200)
    fonction = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    image = models.ImageField()

    def __str__(self):
        return self.nom
    
class AvisClient(models.Model):
    client = models.CharField(max_length=200)
    status = models.CharField(max_length=200, null=True)
    avis = models.CharField(max_length=400)
    image = models.ImageField()

    def __str__(self):
        return self.client
    
class Tarif(models.Model):
    trajet = models.CharField(max_length=200)
    prix = models.CharField(max_length=70)

    def __str__(self):
        return self.trajet

class Agence(models.Model):
    ville = models.CharField(max_length=200)
    agence = models.CharField(max_length=200)
    adresse= models.CharField(max_length=200)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.ville
    
class Profile(models.Model):
    bannier_profile_name = models.CharField(max_length=200)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.bannier_profile_name
    

