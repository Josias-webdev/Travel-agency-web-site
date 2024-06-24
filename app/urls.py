
from django.urls import path 
from . import views

#This will import our view that we have already created
from .views import GeneratePdf

urlpatterns = [
    path('', views.home, name="home"),
    path("agences/", views.agences, name="agences"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("download_pdf/", views.download_pdf, name="download_pdf"),
    path('pdf/', GeneratePdf.as_view()),
]
