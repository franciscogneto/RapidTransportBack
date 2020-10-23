from django.urls import path
from .views import EmpresaAPIView,VeiculoAPIView



urlpatterns = [
    path('veiculos/',VeiculoAPIView.as_view(), name = 'veiculos')
]