from django.contrib import admin
from .models import Empresa,Veiculo,Funcionario,Usuario
# Register your models here.

#igual ao admin.site.register(Nome)
@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("nome","cnpj","telefone")

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ("placa","modelo","color","empresa")
    #customizando a página admin

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    pass

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    pass
