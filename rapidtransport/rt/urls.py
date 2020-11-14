from django.urls import path
from .views import EmpresaAPIView,FuncionarioListaAPIView,FuncionarioDetalheAPIView,UsuarioAPIView,VeiculoListaAPIView,VeiculoDetalheApiView,RelatorioListaAPIView,ItemAPIView,testeItemApiView,RelatorioDetalheAPIView
from .views import LoginView

urlpatterns = [
    path('login/',LoginView.as_view(), name='login'),
    path('veiculos/',VeiculoListaAPIView.as_view(), name = 'veiculos'),
    path('veiculos/<int:id>/',VeiculoDetalheApiView.as_view(),name = 'veiculo'),
    path('funcionarios/',FuncionarioListaAPIView.as_view(), name = 'funcionarios'),
    path('funcionarios/<int:id>/',FuncionarioDetalheAPIView.as_view()),
    path('empresa/',EmpresaAPIView.as_view(), name = 'empresa'),
    path('usuarios/',UsuarioAPIView.as_view(), name = 'usuarios'),
    path('relatorios/',RelatorioListaAPIView.as_view(), name = 'relatorio'),
    path('relatorios/<int:id>/',RelatorioDetalheAPIView.as_view(), name = 'exclui_relatorio'),
    path('itens/',ItemAPIView.as_view(),name = 'itens'),
    path('item/<int:id_item>/',testeItemApiView.as_view(),name = 'exclui_item')
]

