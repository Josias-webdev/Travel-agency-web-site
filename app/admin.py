from django.contrib import admin
from .models import Bannier, Reservation, Apropos, AvisClient, Tarif, Agence, Logo, Profile

# Register your models here.

admin.site.register(Logo)
admin.site.register(Profile)

class BannierAdmin(admin.ModelAdmin):
    list_display = ('nom_bannier', 'sous_titre_bannier', 'titre_bannier', 'texte_bannier')

admin.site.register(Bannier, BannierAdmin)

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'r_nom', 'r_prenom', 'r_piece_nationale', 'r_date', 'r_destination', 'r_provenance', 'r_agences', 'r_phone', 'qr_code', 'payement', 'create_date',)

admin.site.register(Reservation, ReservationAdmin)

class AproposAdmin(admin.ModelAdmin):
    list_display = ('nom', 'fonction', 'description')

admin.site.register(Apropos, AproposAdmin)

class AvisClientAdmin(admin.ModelAdmin):
    list_display = ('id','client', 'status', 'avis')

admin.site.register(AvisClient, AvisClientAdmin)

class TarifAdmin(admin.ModelAdmin):
    list_display = ('trajet', 'prix')

admin.site.register(Tarif, TarifAdmin)

class AgenceAdmin(admin.ModelAdmin):
    list_display = ('ville', 'agence', 'adresse')

admin.site.register(Agence, AgenceAdmin)
