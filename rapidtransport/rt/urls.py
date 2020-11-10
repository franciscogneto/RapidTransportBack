from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import EmpresaAPIView,FuncionarioListaAPIView,FuncionarioDetalheAPIView,UsuarioAPIView,VeiculoListaAPIView,VeiculoDetalheApiView
from .views import LoginView

urlpatterns = [
    path('login/',LoginView.as_view(), name='login'),
    path('veiculos/',VeiculoListaAPIView.as_view(), name = 'veiculos'),
    path('veiculos/<int:id>/',VeiculoDetalheApiView.as_view(),name = 'veiculo'),
    path('funcionarios/',FuncionarioListaAPIView.as_view(), name = 'funcionarios'),
    path('funcionarios/<int:id>/',FuncionarioDetalheAPIView.as_view()),
    path('empresa/',EmpresaAPIView.as_view(), name = 'empresa'),
    path('usuarios/',UsuarioAPIView.as_view(), name = 'usuarios')
]

