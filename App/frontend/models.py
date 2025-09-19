from django.db import models

class filtros(models.Model):
    id = models.AutoField(primary_key=True,name='id')
    variavelInteresse = models.CharField(name="variavel_interesse",max_length=10000,default=None,null=False)
    curso = models.CharField(name="curso",max_length=10000,default="", null= True)
    periodo = models.CharField(name="periodo",max_length=10000,default="",null=True)
    ingresso = models.CharField(name="ingresso",max_length=10000,default="", null= True)
    sexo = models.CharField(name="sexo",max_length=10000,default="", null= True)
    cor = models.CharField(name="cor",max_length=10000,default="", null= True)
    nacionalidade = models.CharField(name="nacionalidade",max_length=10000,default="", null= True)
    cidade_nascimento = models.CharField(name="cidade_nascimento",max_length=10000,default="", null= True)
    cidade_moradia = models.CharField(name="cidade_moradia",max_length=10000,default="", null= True)
    mensagem = models.TextField(name="mensagem",max_length=10000,default=None, null= True)
# Create your models here.
