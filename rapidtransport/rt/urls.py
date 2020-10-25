from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import EmpresaAPIView,VeiculoAPIView,FuncionarioAPIView,VeiculoByIdView,FuncionarioByIdView



urlpatterns = [
    path('veiculos/',VeiculoAPIView.as_view(), name = 'veiculos'),
    path('veiculos/<int:pk>/',VeiculoByIdView.as_view()),
    path('funcionarios/',FuncionarioAPIView.as_view(), name = 'funcionarios'),
    path('funcionarios/<int:pk>/',FuncionarioByIdView.as_view())
]

