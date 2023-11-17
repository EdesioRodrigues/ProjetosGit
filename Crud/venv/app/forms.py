from django import forms
from .models import Clientes, Categoria, EmailTemplate

class EmailTemplateForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = ['subject', 'body']

class ClientesForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['nome', 'email', 'telefone', 'cidade', 'estado', 'init_contrato', 'fim_contrato', 'periodicidade', 'servico', 'tipo', 'setor', 'categoria']


class CategoriaForm(forms.ModelForm):
    nome = forms.CharField(label='Nome da Categoria', max_length=100)

    class Meta:
        model = Categoria
        fields = ['nome']



