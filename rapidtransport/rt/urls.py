from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import EmpresaAPIView,FuncionarioAPIView,FuncionarioByIdView,UsuarioAPIView,VeiculoListaAPIView,VeiculoDetalheApiView


urlpatterns = [
    path('veiculos/',VeiculoListaAPIView.as_view(), name = 'veiculos'),
    path('veiculos/<int:id>/',VeiculoDetalheApiView.as_view(),name = 'veiculo'),
    path('funcionarios/',FuncionarioAPIView.as_view(), name = 'funcionarios'),
    path('funcionarios/<int:id>/',FuncionarioAPIView.as_view()),
    path('empresa/',EmpresaAPIView.as_view(), name = 'empresa'),
    path('usuarios/',UsuarioAPIView.as_view(), name = 'usuarios')
]

