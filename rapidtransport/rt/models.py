from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
#Herda a classe model do django

class Usuario(AbstractUser):
    is_funcionario = models.BooleanField(default=False)
    is_empresa = models.BooleanField(default=False)

    class Meta:
        db_table = "usuarios"
    
class Empresa(models.Model):
    usuario = models.OneToOneField(Usuario,on_delete=models.CASCADE,primary_key=True)
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
    STATUS = (
        (1,'DISPONÍVEL'),
        (2,'AUSENTE'),
        (3,'INOPERANTE')
    )
    id = models.AutoField(primary_key=True)
    modelo = models.CharField(max_length=50)
    color = models.CharField(max_length=25)
    placa = models.CharField(max_length=10,unique=True)
    kilometragem_inicial = models.PositiveIntegerField()
    kilometragem_revisao = models.PositiveIntegerField()
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=STATUS,default=1)
    
    #Como será mostrado este model no admin por exemplo quando criado um novo objeto.
    def __str__(self):
        return self.placa

    class Meta:
        db_table = "veiculos"

class Funcionario(models.Model):
    TIPO_CARTA = (
        ('A', 'MOTO'),
        ('B', 'CARRO'),
        ('C', 'CAMINHÃO'),
        ('D', 'ONIBUS'),
        ('E', 'CARRETA'),
    )
    STATUS = (
        (1,'DISPONÍVEL'),
        (2,'AUSENTE'),
        (3,'INOPERANTE')
    )

    usuario = models.OneToOneField(Usuario,on_delete=models.CASCADE,primary_key=True)
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    data_admissao = models.DateField()
    data_aniversario = models.DateField()
    tipo_carteira = models.CharField(max_length=1,choices=TIPO_CARTA)
    celular = models.CharField(max_length=18)
    cpf = models.CharField(max_length=20,unique=True)
    status = models.PositiveSmallIntegerField(choices=STATUS,default=1)

    def __str__(self):
        return self.nome
    class Meta:
        db_table = "funcionarios"

class Relatorio(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nome

    class Meta:
        db_table = "relatorio"
class Item(models.Model):   
    TIPO_GRAU = (
        (1,'LEVE'),
        (2,'MODERADO'),
        (3,'URGENTE'),
    )
    id = models.AutoField(primary_key=True)
    relatorio = models.ForeignKey(Relatorio,on_delete=models.CASCADE)
    grau_emergencia = models.PositiveSmallIntegerField(choices=TIPO_GRAU,default=1)
    descricao = models.CharField(max_length=200)
    check = models.BooleanField(default=False)

    def __str__(self):
        return "item"
    class Meta:
        db_table = "item"

class Viagem(models.Model):
    id = models.AutoField(primary_key=True)
    origem = models.CharField(max_length=200)
    destino = models.CharField(max_length=200)
    carga = models.CharField(max_length=100)
    viagem_finalizada = models.BooleanField(default=False)
    data_inicio = models.DateField()
    periodizacao_relatorio = models.SmallIntegerField()
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario,on_delete=models.CASCADE)
    veiculo = models.ForeignKey(Veiculo,on_delete=models.CASCADE)
    

    class Meta:
        db_table = "viagem"
class Relatorios_Viagem(models.Model):
    id = models.AutoField(primary_key=True)
    relatorio = models.ForeignKey(Relatorio,on_delete=models.CASCADE)
    viagem = models.ForeignKey(Viagem,on_delete=models.CASCADE)
    data_preenchimento = models.DateField(null=True)
    observacao = models.CharField(max_length=300,blank=True,null=True)
