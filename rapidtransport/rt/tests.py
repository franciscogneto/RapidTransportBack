from django.test import TestCase, Client
from .regularizadores.auxiliar import GeraSenhaUsuario,RegularizaViagem


class TesteRegularizadores(TestCase):

    def teste_senhas_geradas(self):#analisando se senha tem o formato correto
        teste = False
        qtd_letra = 0
        qtd_numero = 0
        senha = GeraSenhaUsuario().gera_senha()
        for letra in senha:
            if(letra >= '0' and letra <= '9'):
                qtd_numero += 1
            elif letra >= 'a' and letra <= 'z':
                qtd_letra += 1
        if(qtd_numero != 4 and qtd_letra != 10):
            teste = True
        self.assertFalse(teste, 'Senha padronizada de forma incorreta')
        self.assertTrue(teste, 'Senha padronizada de forma correta')


    def teste_login(self):
        teste = False
        c = Client()
        objeto = {
            'username': '6542476000137',
            'password': '1122'
        }
        resposta = c.post('http://127.0.0.1:8000/api/login/',data=objeto)      
        self.assertEquals(200,resposta.status_code,'logado com sucesso')
        self.assertEquals(401,resposta.status_code,'não foi possível')
        
