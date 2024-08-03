
from django.urls import path, include
from . import views

#This will import our view that we have already created
from .views import GeneratePdf

urlpatterns = [
    path('', views.home, name="home"),
    path("agences/", views.agences, name="agences"),
    path("signin", views.signin, name="signin"),
    path("signup", views.signup, name="signup"),
    path("profile", views.profile, name="profile"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("signout", views.signout, name="signout"),
    path("activation/<uidb64>/<token>", views.activation, name="activation"),
    path("reservation_pdf", views.reservation_pdf, name="reservation_pdf"),
    path("download_pdf/", views.download_pdf, name="download_pdf"),
    path('pdf/', GeneratePdf.as_view()),
]
