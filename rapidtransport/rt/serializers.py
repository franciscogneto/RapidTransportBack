from rest_framework import serializers
from .models import Empresa,Veiculo,Funcionario,Usuario



class EmpresaSerializer(serializers.ModelSerializer):



    class Meta:
        """extra_kargs = { #alguns dados são comercializados, sendo assim é bom protege-los
            'cnpj': {'write_only':True},
            'endereco': {'write_only':True},
            'telefone': {'write_only':True}
        }"""
        model = Empresa #model que estou utilziando
        fields = ( #seus campos
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
        fields = (
            'id',
            'modelo',
            'color',
            'placa',
            'kilometragem_inicial',
            'kilometragem_revisao',
            'empresa'
        )
    


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
            'celular'
        )