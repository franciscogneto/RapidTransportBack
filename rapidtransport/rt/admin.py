from django.contrib import admin
from .models import Empresa,Veiculo
# Register your models here.

#igual ao admin.site.register(Nome)
@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("nome","cnpj","telefone")

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ("placa","modelo","color","empresa")
    #customizando a página admin
