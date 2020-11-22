from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Empresa,Veiculo,Funcionario,Usuario,Relatorio,Item,Revisao,Viagem,Relatorios_Viagem
from .serializers import EmpresaSerializer,VeiculoSerializer,FuncionarioSerializer,UsuarioSerializer
from .serializers import RelatorioSerializer,ItemSerializer,RevisaoSerializer,ViagemSerializer,Relatorio_ViagemSerializer
from django.core import serializers
from django.contrib.auth.hashers import make_password,check_password
from .permissions.permissions import IsEmpresaUser,IsFuncionarioUser,IsSuperUser
from .regularizadores.auxiliar import GeraSenhaUsuario,RegularizadorVeiculo
from .regularizadores.auxiliar import RegularizaFuncionario,RegularizaRelatorio_Itens,RegularizaViagem
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken 
from datetime import datetime

class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):
        username = request.data['username']
        password = request.data['password']
        
        if(Usuario.objects.filter(username=username).exists()):
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
            resposta = 'usuário: '+ request.data['username']
            return Response(status=status.HTTP_401_UNAUTHORIZED,data='usuario ou senha incorreto') 

    def token_para_usuario(self,usuario):
        refresh = RefreshToken.for_user(usuario)
        
        return{
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class EmpresaAPIView(APIView):
    permission_classes = (IsSuperUser,)

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
                password=GeraSenhaUsuario.gera_senha(),
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
    permission_classes = (IsSuperUser,)

    def get(self,request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios,many=True)
        return Response(data=serializer.data)

#############################################

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
            funcionario = Funcionario.objects.get(usuario=id)
            viagem = Viagem.objects.filter(funcionario=funcionario).filter(viagem_finalizada=False)
            status = int(request.data['status'])
            if(viagem.exists()):
                if(status != funcionario.status and status == 1):
                    return Response(status=sta)
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


class RelatorioListaAPIView(APIView):
    permission_classes = (AllowAny,)
    
    def get(self,request):
        serializer = RelatorioSerializer(Relatorio.objects.all(),many=True)
        return Response(data=serializer.data)
    
    def post(self,request):
        relatorio = request.data['relatorio']  
        print(relatorio)      
        itens = request.data['itens']
        print(itens)
        aux_existe = False
        if(RegularizaRelatorio_Itens().regulariza_relatorio(relatorio,itens)):
            relatorio_salvo = Relatorio.objects.create(nome=relatorio['nome'])
            for item in itens:
                Item.objects.create(descricao=item['descricao'],relatorio=relatorio_salvo)
                aux = str(item['descricao'])
                aux = aux.upper()
                if(aux == 'ODOMETRO' or aux == 'ODÓMETRO' or aux == 'ODÔMETRO'):
                    aux_existe = True
            if(not(aux_existe)):
                Item.objects.create(descricao='Odómetro',relatorio=relatorio_salvo)
            return Response(status=status.HTTP_200_OK,data='Salvo com sucesso')
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data='Não foi possível salvar, verifique os dados')


class RelatorioDetalheAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request,id):
        relatorio = Relatorio.objects.filter(id=id)
        if(relatorio.exists()):
            serializer_itens = ItemSerializer(Item.objects.filter(relatorio=relatorio[0]),many=True)
            serializer = RelatorioSerializer(relatorio[0])
            resposta = {
                'relatorio': serializer.data,
                'itens': serializer_itens.data
            }
            return Response(status=status.HTTP_200_OK,data=resposta)
        return Response(status=status.HTTP_400_BAD_REQUEST,data='relatório inexistente')

    def delete(self,request,id):
        #conferir se tem alguma viagem com este relatório
        relatorio = Relatorio.objects.filter(id=id)
        if(relatorio.exists()):
            for item in Item.objects.filter(relatorio=relatorio[0]):
                item.delete()
            nome_relatorio = relatorio[0].nome
            relatorio[0].delete()
            mensagem = 'relatório: '+nome_relatorio.upper()+' excluído com sucesso'
            return Response(status=status.HTTP_204_NO_CONTENT, data=mensagem)
        return Response(status=status.HTTP_400_BAD_REQUEST,data='relatório inexistente')


class ItemAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request):
        serializer = ItemSerializer(Item.objects.all(),many=True)
        return Response(data=serializer.data)

    """def delete(self,request,id_item):
        #conferir se tem alguma viagem com o relatório deste item
        if(Item.objects.filter(id=id_item).exists()):
            Item.objects.get(id=id_item).delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST,data='Item inexistente')"""


class testeItemApiView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request,id_item):
        item = Item.objects.filter(id=id_item)
        if(item.exists()):
            serializer = ItemSerializer(item[0])
            return Response(data=serializer.data)
        return Response(data='item inexistente')

    def delete(self,request,id_item):
        #conferir se tem alguma viagem com o relatório deste item
        item = Item.objects.filter(id=id_item) 
        if(item.exists()):
            item[0].delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class RevisaoListaAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request,id_veiculo):
        veiculo = Veiculo.objects.filter(id=id_veiculo)
        if(veiculo.exists()):
            veiculo = veiculo[0]
            revisoes = Revisao.objects.filter(veiculo = veiculo)
            if(revisoes.__len__() > 0):
                serializer = RevisaoSerializer(revisoes, many=True)
                return Response(status=status.HTTP_200_OK, data=serializer.data)
            return Response(status=status.HTTP_400_BAD_REQUEST, data='este veículo não possuí revisões')
        return Response(status=status.HTTP_400_BAD_REQUEST, data='veículo inexistente')

    def post(self,request,id_veiculo):
        veiculo = Veiculo.objects.filter(id=id_veiculo)
        
        if(veiculo.exists()):
            veiculo = veiculo[0]
            request.data['veiculo'] = veiculo.id
            revisao = RevisaoSerializer(data=request.data)
            if(revisao.is_valid()):
                if(not(Revisao.objects.filter(veiculo=veiculo).exists())):
                    revisao.save()
                    return Response(status=status.HTTP_200_OK, data='revisão criada com sucesso')
                if( revisao.validated_data['data'] > veiculo.data_registro):
                    revisoes = Revisao.objects.filter(veiculo=veiculo).filter(data__gt=revisao.validated_data['data'])#data > 
                    if(not(revisoes.exists())):
                        revisao_aux = Revisao.objects.filter(veiculo=veiculo).latest('data')
                        if(revisao_aux.kilometragem <= int(revisao.validated_data['kilometragem'])):
                            if(int(revisao.validated_data['nota']) >= 0 and int(revisao.validated_data['nota'] <= 10)):
                                revisao.save()
                                return Response(status=status.HTTP_200_OK, data='revisão criada com sucesso')
                return Response(status=status.HTTP_400_BAD_REQUEST, data='check os dados inseridos')
            return Response(revisao.errors)

class RevisaoDetalheAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request,id_revisao):
        revisao = Revisao.objects.filter(id = id_revisao)
        if(revisao.exists()):
            revisao = revisao[0]
            serializer = RevisaoSerializer(revisao)
            return Response(status=status.HTTP_200_OK,data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST,data='revisão inexistente')

class ViagemListaAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request):
        serializer = ViagemSerializer(Viagem.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK,data=serializer.data)
    
    def post(self,request):
        viagem_serializer = ViagemSerializer(data=request.data['viagem'])
        if(viagem_serializer.is_valid()):
            funcionario = Funcionario.objects.filter(usuario=viagem_serializer.validated_data['funcionario'])
            veiculo = Veiculo.objects.filter(id=viagem_serializer.validated_data['veiculo'].id)
            relatorio = Relatorio.objects.filter(id = request.data['relatorio'])
            if(funcionario.exists() and veiculo.exists() and relatorio.exists()):
                funcionario = funcionario[0]
                veiculo = veiculo[0]
                relatorio = relatorio[0]
                # se igual a disponível
                if(funcionario.status == 1 and veiculo.status == 1): 
                    if(RegularizaViagem.regulariza_viagem(RegularizaViagem,viagem_serializer.validated_data['origem'],viagem_serializer.validated_data['destino'],viagem_serializer.validated_data['carga'],viagem_serializer.validated_data['periodizacao_relatorio'],viagem_serializer.validated_data['data_inicio'])):
                        viagem = viagem_serializer.save()
                        relatorio_viagem = Relatorios_Viagem.objects.create(viagem=viagem,relatorio=relatorio)
                        funcionario.status = 3
                        veiculo.status = 3
                        funcionario.save()
                        veiculo.save()
                        return Response(data='viagem criada com sucesso!')
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST, data='check os dados inseridos')
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data='veículo ou funcionário indisponível')
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data='veículo, funcionário ou relatório inexistente')
        return Response(viagem_serializer.errors)

class ViagemDetalheAPIView(APIView):
    permission_classes = (AllowAny,)
    
    def get(self,request,id):
        viagem = Viagem.objects.filter(id=id)
        if(viagem.exists()):
            viagem = viagem[0]
            serializer = ViagemSerializer(viagem)
            return Response(status=status.HTTP_200_OK,data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data='Viagem inexistente')
    
    def delete(self,request,id):
        viagem = Viagem.objects.filter(id=id)
        if(viagem.exists()):
            relatorios_viagens = Relatorios_Viagem.objects.filter(viagem=viagem[0])
            if(relatorios_viagens.__len__() == 1):
                relatorios_viagens = relatorios_viagens[0]
                funcionario = relatorios_viagens.viagem.funcionario
                veiculo = relatorios_viagens.viagem.veiculo
                viagem = relatorios_viagens.viagem
                
                funcionario.status = 1
                funcionario.save()
                
                veiculo.status = 1
                veiculo.save()
                
                viagem.delete()
                relatorios_viagens.delete()

                return Response(data='Viagem excluída com sucesso')
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST,data='Não foi possível excluir está viagem pois possui relatórios associados')
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data='Viagem inexistente')





