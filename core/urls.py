from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name="index"),
    path('Handle_Form/', views.Handle_Form, name="Handle_Form"),

]