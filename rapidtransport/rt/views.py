from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Empresa,Veiculo,Funcionario,Usuario
from .serializers import EmpresaSerializer,VeiculoSerializer,FuncionarioSerializer,UsuarioSerializer
from django.core import serializers
from django.contrib.auth.hashers import make_password,check_password
from .permissions.permissions import IsEmpresaUser,IsFuncionarioUser
from .regularizadores.auxiliar import GeraSenhaUsuario,RegularizadorVeiculo,RegularizaFuncionario
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken 
# Create your views here.


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):
        username = request.data['username']
        password = request.data['password']
        usuario = Usuario.objects.get(username=username)
        if(usuario.check_password(password)):
            jwt = LoginView.token_para_usuario(LoginView,usuario)
            if(usuario.is_empresa):
                resposta = {
                    'refresh': str(jwt['refresh']),
                    'access': str(jwt['access']),
                    'isFuncionario': 0,
                    'isEmpresa':1,
                }
                return Response(status=status.HTTP_200_OK,data=resposta)
            elif(usuario.is_funcionario):
                resposta = {
                    'refresh': str(jwt['refresh']),
                    'access': str(jwt['token']),
                    'isFuncionario': 1,
                    'isEmpresa':0,
                }
                return Response(status=status.HTTP_200_OK,data=resposta)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST,data="Erro no Login, refaça a operação")#formatação incorreta
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED,data="usuário ou senha incorreto") 

    def token_para_usuario(self,usuario):
        refresh = RefreshToken.for_user(usuario)
        
        return{
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class EmpresaAPIView(APIView):
    permission_classes = (AllowAny,)

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
        serializer = UsuarioSerializer(usuarios,many=True)
        return Response(data=serializer.data)

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

class FuncionarioListaAPIView(APIView):

    permission_classes = (AllowAny,)


    def get(self,request):
        funcionario = Funcionario.objects.all()
        serializer = FuncionarioSerializer(funcionario,many=True)
        return Response(serializer.data)

    def post(self,request):

        if(not(Funcionario.objects.filter(cpf=request.data['cpf']).exists())):
            print(request.data['cpf'])
            if(RegularizaFuncionario.regulariza_funcionario(RegularizaFuncionario,request.data['cpf'],request.data['nome'],request.data['celular'],request.data['data_aniversario'],request.data['data_admissao'])):
                if(not(Empresa.objects.filter(usuario=request.data['empresa']).exists())):
                    return Response(status=status.HTTP_400_BAD_REQUEST, data="não foi possível criar o funcionários, check os dados")
                empresa_aux = Empresa.objects.get(usuario=request.data['empresa'])
                senha = GeraSenhaUsuario.gera_senha(GeraSenhaUsuario)
                usuario = Usuario.objects.create(username=request.data['cpf'],password=make_password(senha))
                funcionario  = Funcionario.objects.create(usuario=usuario,
                nome=request.data['nome'],
                data_admissao=request.data['data_admissao'],
                data_aniversario=request.data['data_aniversario'],
                tipo_carteira=request.data['tipo_carteira'],
                celular=request.data['celular'],
                cpf= request.data['cpf'],
                empresa= empresa_aux
                )
                data = {
                    'usuario' : request.data['cpf'],
                    'senha' : senha
                }
                return Response(status=status.HTTP_201_CREATED,data=data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data="não foi possível criar o funcionários, check os dados")
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data="cpf já existente")

class FuncionarioDetalheAPIView(APIView):
    permission_classes = (AllowAny,)
    def get(self,request,id):
        if(Funcionario.objects.filter(usuario=id)):
            funcionario = Funcionario.objects.get(usuario=id)
            serializer = FuncionarioSerializer(funcionario)
            return Response(status=status.HTTP_200_OK,data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST,data="funcionário inexistente")
    
    def put(self,request,id):
        if(Funcionario.objects.filter(usuario=id).exists()):
            if(RegularizaFuncionario.regulariza_funcionario(RegularizaFuncionario,request.data['cpf'],request.data['nome'],request.data['celular'],request.data['data_aniversario'],request.data['data_admissao'])):
                usuarios = Usuario.objects.filter(username=request.data['cpf'])
                for usuario in usuarios:  
                    if(usuario.username == request.data['cpf'] and usuario.id != id):
                        return Response(status=status.HTTP_400_BAD_REQUEST,data='não foi possível a atualização do funcionário, porfavor check os dados inseridos')
                funcionario = Funcionario.objects.get(usuario=usuarios[0])
                serializer = FuncionarioSerializer(funcionario, data=request.data)
                if(serializer.is_valid()):
                    serializer.save()
                    return Response(status=status.HTTP_200_OK,data=serializer.data)
                else:
                    return Response(serializer.errors)
                
        return Response(status=status.HTTP_400_BAD_REQUEST,data='não foi possível a atualização do funcionário, porfavor check os dados inseridos')
    
    def delete(self,request,id):
        if(Funcionario.objects.filter(usuario=id).exists()):
            usuario = Usuario.objects.get(id=id)
            funcionario = Funcionario.objects.get(usuario=usuario)
            mensagem = "excluído com sucesso funcionário: nome:"+funcionario.nome+" cpf: "+funcionario.cpf
            funcionario.delete()
            usuario.delete()
            return Response(status=status.HTTP_204_NO_CONTENT , data=mensagem)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data="funcionário não encontrado")