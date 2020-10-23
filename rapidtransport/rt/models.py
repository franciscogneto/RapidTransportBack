from django.db import models

# Create your models here.
#Herda a classe model do django



class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=20)
    endereco = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome
    
    #classe para configurações
    class Meta:
        db_table = "empresa"   


class Veiculo(models.Model):
    modelo = models.CharField(max_length=50)
    color = models.CharField(max_length=25)
    placa = models.CharField(max_length=10)
    kilometragem_inicial = models.PositiveIntegerField()
    kilometragem_revisao = models.PositiveSmallIntegerField()
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE)
    
    #Como será mostrado este model no admin por exemplo quando criado um novo objeto.
    def __str__(self):
        return self.placa

    class Meta:
        db_table = "veiculos"



