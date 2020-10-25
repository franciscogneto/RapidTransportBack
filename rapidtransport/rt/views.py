from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Empresa,Veiculo,Funcionario
from .serializers import EmpresaSerializer,VeiculoSerializer,FuncionarioSerializer

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

    def put(self,request):
        serializer = VeiculoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
    
class VeiculoByIdView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    """def get_object(self,pk):
        veiculo = Veiculo.objects.get(id = pk)
        serializer = VeiculoSerializer(veiculo)
        return Response(serializer.data)"""

class FuncionarioAPIView(APIView):

    def get(self,request):
        funcionario = Funcionario.objects.all()
        serializer = FuncionarioSerializer(funcionario,many=True)
        return Response(serializer.data)


class FuncionarioByIdView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer