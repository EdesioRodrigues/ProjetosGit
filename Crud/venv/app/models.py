from django.db import models

class EmailTemplate(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField(help_text="Corpo do email em formato HTML")

    def save(self, *args, **kwargs):
        if not self.id:
            last_id = EmailTemplate.objects.all().order_by('id').last()
            if last_id:
                self.id = last_id.id + 1
            else:
                self.id = 1
        super(EmailTemplate, self).save(*args, **kwargs)

    def __str__(self):
        return self.subject
    
class Tipo(models.Model):
    TIPO_CHOICES = (
        ('casa', 'Casa'),
        ('empresa', 'Empresa'),
        ('industria', 'Indústria'),
    )
    nome = models.CharField(max_length=50, null=True, choices=TIPO_CHOICES)

    def __str__(self):
        return self.nome
    
class Periodicidade(models.Model):
    TIPO_CHOICES = (
        ('semanal', 'Semanal'),
        ('quinzenal', 'Quinzenal'),
        ('mensal', 'Mensal'),
        ('bimestral', 'Bimestral'),
        ('trimestral', 'Trimestral'),
        ('quadrimestral', 'Quadrimestral'),
        ('semestral', 'Semestral'),
        ('anual', 'Anual'),
    )
    nome = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.nome or "Sem nome definido"
    
class Servicos(models.Model):
    TIPO_CHOICES = (
        ('MIVP ', 'MIVP '),
        ('CDR ', 'CDR '),
        ('HDR ', 'HDR '), 
         ('CMA ', 'CMA '),  
    )
    nome = models.CharField(max_length=50, choices=TIPO_CHOICES)

    def __str__(self):
        return self.nome


class Categoria(models.Model):
    nome = models.CharField(max_length=50, null=True, blank=True, unique=True)

    def __str__(self):
        return self.nome

class Clientes(models.Model):
    nome = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=40, null=True, blank=True)
    telefone = models.IntegerField(null=True, blank=True)
    cidade = models.CharField(max_length=50, null=True, blank=True)
    estado = models.CharField(max_length=50, null=True, blank=True)
    init_contrato = models.DateField(null=True, blank=True)
    fim_contrato = models.DateField(null=True, blank=True)
    periodicidade = models.ForeignKey(Periodicidade, on_delete=models.SET_NULL, null=True, blank=True)
    servico = models.ForeignKey(Servicos, on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.ForeignKey(Tipo, on_delete=models.SET_NULL, null=True, blank=True)
    setor = models.CharField(max_length=50, null=True, blank=True)
    categoria = models.ManyToManyField(Categoria)

    def __str__(self):
        return self.nome
    
