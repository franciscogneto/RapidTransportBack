




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