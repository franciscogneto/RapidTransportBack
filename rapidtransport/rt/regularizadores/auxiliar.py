from datetime import datetime,date
from random import randint



class RegularizadorVeiculo():
    def regulariza_veiculo(self,modelo: str,cor: str,placa: str,):
        modelo = modelo.replace(' ','')
        cor = cor.replace(' ','')
        placa = placa.replace(' ','')
        placa = placa.upper()
        i = 0
        if(modelo.__len__() > 0):
            if(cor.__len__() > 2):
                if(placa[3] == '-'):
                    while(i < placa.__len__()):
                        if(i < 3):
                            if( not(placa[i] >= 'A' and placa[i] <= 'Z')):
                                return False
                        if(i > 3):
                            if(not(placa[i] >= '0' and placa[i] <= '9')):
                                return False
                        i+=1
                else:
                    return False
        return True


class RegularizaFuncionario():
    def regulariza_funcionario(self,cpf: str,nome: str,celular: str,data_aniversario: datetime,data_admissao: datetime):
        print("ENTROUUU")
        idade = RegularizaFuncionario.calcula_idade(self,data_aniversario)
        print(idade)
        admissao = RegularizaFuncionario.calcula_idade(self,data_admissao)
        print(admissao)
        aux_celular = celular.replace('','')
        if(cpf.__len__() > 8):
            if(nome.__len__() > 5):
                if(aux_celular.__len__() > 8):
                    if(idade > 24 and admissao < idade):
                        if(15 <= (idade - admissao)):
                            return True                    
        
        return False

    
    def calcula_idade(self,data_aniversario: datetime):
        hoje = datetime.today()
        ano = hoje.year
        data_atual = date(hoje.year,hoje.month,hoje.day)
        data_aniversario_aux = datetime.strptime(data_aniversario, '%Y-%m-%d').date()
        idade = (data_atual - data_aniversario_aux)
        idade = idade.days/365.25
        idade = idade.__int__()

        return idade

    
    """def verifica_update_senha(self,senha:str):
        i = 0
        qtd_caractere = 0
        qtd_numero = 0
        while(i < senha.__len__()):
            if(i == 0):

            else:"""

class GeraSenhaUsuario():
    
    def gera_senha(self):
        i = 1;
        senha = GeraSenhaUsuario.gera_letra(self)
        while(i < 14):
            if( i < 10):
                senha += GeraSenhaUsuario.gera_letra(self)
            else:
                senha += GeraSenhaUsuario.gera_numero(self)
            i+=1
        senha += ""
        #print(senha)
        return senha

    def gera_numero(self):
        return chr(randint(a=48,b=57))
    
    def gera_letra(self):
        return chr(randint(a=97,b=122))
            