from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientes, name="clientes"),
    path('Atualiza_cliente/', views.att_clientes, name="atualiza_cliente")
]