from rest_framework import serializers
from .models import Empresa,Veiculo



class EmpresaSerializer(serializers.ModelSerializer):

    class Meta:
        """extra_kargs = { #alguns dados são comercializados, sendo assim é bom protege-los
            'cnpj': {'write_only':True},
            'endereco': {'write_only':True},
            'telefone': {'write_only':True}
        }"""
        model = Empresa #model que estou utilziando
        fields = ( #seus campos
            'id',
            'nome',
            'cnpj',
            'endereco',
            'telefone'
        )


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