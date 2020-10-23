from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Empresa,Veiculo
from .serializers import EmpresaSerializer,VeiculoSerializer

# Create your views here.

class EmpresaAPIView(APIView):

    def get(self,request):
        empresas = Empresa.objects.all()
        serializer = EmpresaSerializer(empresas, many=True)
        return Response(serializer.data)


class VeiculoAPIView(APIView):


    def get(self,request):
        veiculos = Veiculo.objects.all()
        serializer = VeiculoSerializer(veiculos, many=True)
        return Response(serializer.data)
