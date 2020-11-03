from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Empresa,Veiculo,Funcionario,Usuario
from .serializers import EmpresaSerializer,VeiculoSerializer,FuncionarioSerializer,UsuarioSerializer
from django.core import serializers
from django.contrib.auth.hashers import make_password
from .permissions.permissions import IsEmpresaUser,IsFuncionarioUser
from .regularizadores.regularizadorVeiculo import RegularizadorVeiculo
# Create your views here.

class EmpresaAPIView(APIView):
    permission_classes = (IsEmpresaUser,)

    def get(self,request):
        empresas = Empresa.objects.all()
        serializer = EmpresaSerializer(empresas, many=True)
        return Response(serializer.data)

    def put(self,request):
        
        serializer = EmpresaSerializer(data=request.data)
        
        if(serializer.is_valid()):
            
            try:
                usuarioAux = Usuario.objects.get(username=serializer.data['cnpj']) 
            except Usuario.DoesNotExist:
                usuarioAux = None
            if usuarioAux == None:
                usuario = Usuario.objects.create(username=serializer.data['cnpj'],
                password=make_password('112233'),
                is_empresa=True,is_active=True)
                empresa = Empresa.objects.create(usuario=usuario,nome=serializer.data['nome'],
                cnpj=serializer.data['cnpj'],
                endereco=serializer.data['endereco'],
                telefone=serializer.data['telefone'])
                return Response(status=status.HTTP_200_OK, data=EmpresaSerializer(empresa,many=False).data)           
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST,data="cadastro existente")        
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
          
class UsuarioAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(data=usuarios,many=True)
        return Response(serializer.data)

############################################# final dos teste e começo das views

class VeiculoListaAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request):
        veiculos = Veiculo.objects.all()
        serializer = VeiculoSerializer(veiculos,many=True)
        return Response(status=status.HTTP_200_OK,data=serializer.data)

    def post(self,request):
        if(RegularizadorVeiculo.regulariza_veiculo(RegularizadorVeiculo,request.data['modelo'],request.data['color'],request.data['placa'])):
            if(not(Veiculo.objects.filter(placa = request.data['placa']).exists())):#caso não exista um veículo com a placa em questão
                serializer = VeiculoSerializer(data=request.data)
                if(serializer.is_valid()):
                    serializer.save()
                    return Response(status=status.HTTP_201_CREATED,data="criado com sucesso")
                else:
                    return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST,data="placa já existente")
        return Response(status=status.HTTP_400_BAD_REQUEST, data="não possível criar o veículo, check os dados")


class VeiculoDetalheApiView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request,id):
        if(Veiculo.objects.filter(id=id).exists()):
            veiculo = Veiculo.objects.get(id=id)
            serializer = VeiculoSerializer(veiculo, many=False)
            return Response(status=status.HTTP_200_OK,data=serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data="veículo não encontrado")

    def put(self,request,id):
        if(Veiculo.objects.filter(id=id).exists()):
            veiculo = Veiculo.objects.get(id=id)
            if(RegularizadorVeiculo.regulariza_veiculo(RegularizadorVeiculo,request.data['modelo'],request.data['color'],request.data['placa'])):
                for objeto in Veiculo.objects.filter(placa=request.data['placa']):
                    if(objeto.id != id):
                        return Response(status=status.HTTP_400_BAD_REQUEST, data="placa já existente no sistema")      
                serializer = VeiculoSerializer(veiculo, data=request.data)
                if(serializer.is_valid()):
                    serializer.save()
                    return Response(status=status.HTTP_202_ACCEPTED, data=serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST,data="não foi possível atualizar os veículo, check os dados")
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="veículo não encontrado")

    def delete(self,request,id):
        if(Veiculo.objects.filter(id=id).exists()):
            veiculo = Veiculo.objects.get(id=id)
            Veiculo.objects.filter(id=id).delete()
            mensagem = "excluído com sucesso veículo da placa "+veiculo.placa
            return Response(status=status.HTTP_204_NO_CONTENT , data=mensagem)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data="veículo não encontrado")

class FuncionarioAPIView(APIView):

    permission_classes = (AllowAny,)

    def get_object(self,request,pk):
        funcionario = Funcionario.objects.get(id=pk)
        serializer = FuncionarioSerializer(funcionario)
        return Response(status=status.HTTP_200_OK,data=serializer.data)

    def get(self,request):
        funcionario = Funcionario.objects.all()
        serializer = FuncionarioSerializer(funcionario,many=True)
        return Response(serializer.data)


class FuncionarioByIdView(generics.RetrieveUpdateDestroyAPIView):#opção de alterar,pegar e deletar
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer

