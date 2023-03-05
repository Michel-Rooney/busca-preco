from django.db import models


class Produto(models.Model):
    id_produto = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255)
    preco = models.DecimalField(decimal_places=2, max_digits=12)
    site = models.TextField(max_length=255)
    data_cotacao = models.DateField()
    link_imagem = models.TextField(max_length=500, default='https://via.placeholder.com/150')

    def __str__(self):
        return f'{self.id_produto} | {self.nome}'