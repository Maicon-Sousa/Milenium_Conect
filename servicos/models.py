from email.policy import default
from secrets import token_hex, token_urlsafe
from django.db import models
from .choices import ChoicesCategoriaManutencao
from clientes.models import Cliente
from datetime import datetime


class CategoriaManutencao(models.Model):
    titulo = models.CharField(max_length=3, choices=ChoicesCategoriaManutencao.choices)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return self.titulo
    
class Servico(models.Model):
    titulo = models.CharField(max_length=100)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    categoria_manutencao = models.ManyToManyField(CategoriaManutencao)
    data_inicio = models.DateField(null=True)
    data_entrega = models.DateField(null=True)
    finalizado = models.BooleanField(default=False)
    protocolo = models.CharField(max_length=52, null=True, blank=True)
    identificador = models.CharField(max_length=24, null=True, blank=True)
    
    
    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        if not self.protocolo:
            self.protocolo = datetime.now().strftime("%d/%m/%Y-%H:%M:%S-") + token_hex(16)  # Gera um protocolo único baseado na data e hora
            
        if not self.identificador: 
            self.identificador = token_urlsafe(16)  # Gera um identificador único para o serviço
            
        super(Servico, self).save(*args, **kwargs)  # Salva o serviço para gerar o ID
        
    def preco_total(self):
        preco_total = float(0)
        for categoria in self.categoria_manutencao.all():
            preco_total += float(categoria.preco)
            
        return preco_total