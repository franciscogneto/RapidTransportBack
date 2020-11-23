from rest_framework import serializers
from .models import Empresa,Veiculo,Funcionario,Usuario,Viagem,Relatorio,Item,Revisao,Viagem,Relatorios_Viagem



class EmpresaSerializer(serializers.ModelSerializer):



    class Meta:
        """extra_kargs = { #alguns dados são comercializados, sendo assim é bom protege-los
            'cnpj': {'write_only':True},
            'endereco': {'write_only':True},
            'telefone': {'write_only':True}
        }"""
        model = Empresa #model que estou utilziando
        fields = ( #seus campos
            'usuario',
            'nome',
            'cnpj',
            'endereco',
            'telefone'
        )
        #fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        

class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = '__all__'
    


class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = (
            'usuario',
            'empresa',
            'nome',
            'data_admissao',
            'data_aniversario',
            'tipo_carteira',
            'celular',
            'cpf',
            'status'
        )

class RelatorioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Relatorio
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'


class RevisaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Revisao
        fields = '__all__'

class ViagemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Viagem
        fields = '__all__'

class Relatorio_ViagemSerializer(serializers.ModelSerializer):

    class Meta:
        models = Relatorios_Viagem
        fields = '__all__'