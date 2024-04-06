from django.db import models


class Carregamento(models.Model):
    data_carregamento = models.DateTimeField(auto_now_add=True, blank=False)
    data_entrega = models.DateTimeField(blank=True)
    quantidade_pallets = models.IntegerField(blank=False)
    empresa_origem = models.CharField(blank=False, max_length=50)
    empresa_destino = models.CharField(blank=False, max_length=50)
    numero_nota_fiscal = models.CharField(blank=False, max_length=50)
    motorista = models.CharField(blank=False, max_length=50)
    venda_ou_descarte = models.BooleanField(blank=True)
