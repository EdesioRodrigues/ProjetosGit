from django.shortcuts import render, redirect, get_object_or_404
from app.forms import ClientesForm
from app.models import Clientes, Categoria, Tipo, Periodicidade, Servicos
from django.db.models import Count
from django.core.paginator import Paginator


from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CategoriaForm
from openpyxl import load_workbook
from datetime import datetime
import re
from .utils import export_to_excel
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from sendgrid.helpers.mail import Mail
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Attachment, FileContent, FileName, FileType, Disposition, Mail
import base64
from .models import EmailTemplate
from .forms import EmailTemplateForm
from django.http import JsonResponse
import openpyxl
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

@login_required
def crud(request):
    data = {}
    search = request.GET.get('search')
    
    if search:
        search_results = Clientes.objects.filter(nome__icontains=search)
        paginator = Paginator(search_results, 2)
        page = request.GET.get('page')
        data['db'] = paginator.get_page(page)
    else:
        all_clients = Clientes.objects.all().order_by('nome')    
        paginator = Paginator(all_clients, 2)
        page = request.GET.get('page')
        data['db'] = paginator.get_page(page)

    return render(request, 'index.html', data)



def form(request):
    date = {}
    date ['form'] = ClientesForm()
    return render(request, 'form.html', date)
    

def create(request):
    form = ClientesForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')
    else:
        return render(request, 'home.html', {'form': form})

    
def view(request, pk):
        date = {}
        date['db'] = Clientes.objects.get(pk = pk)
        return render(request, 'view.html', date)

def edit(request, pk):
     date = {}
     date['db'] = Clientes.objects.get(pk = pk)
     date['form'] = ClientesForm(instance=date['db'])
     return render(request, 'form.html', date)

def update(request, pk):
     date = {}
     date['db'] = Clientes.objects.get(pk = pk)
     form = ClientesForm(request.POST or None, instance=date['db'])
     if form.is_valid():
          form.save()
     return redirect('home')

def delete(request, pk):
     db = Clientes.objects.get(pk = pk)
     db.delete()
     return redirect('crud')

def home(request):
     return render(request, 'home.html')

@login_required
def cadastro(request):
     if request.method == 'GET':
          return render(request, 'cadastro.html', {
               'form': UserCreationForm
          })
     
     else:
          if request.POST['password1'] == request.POST['password2']:
               try:
                    
                    user = User.objects.create_user(username=request.POST['username'], password = request.POST['password1'])
                    user.save()

                    login(request, user)
                    return redirect('crud')
               
               except:
                    return render(request, 'cadastro.html', {
                    'form': UserCreationForm,
                    "error": 'Usuário já existe!!'
                    
                   })
               
          return render(request, 'cadastro.html',{
                      'form': UserCreationForm,  
                      "error": 'Senhas são diferentes!!'
                      })
     
def logar(request):
     if request.method == 'GET':
            return render(request, 'logar.html', {
                 'form': AuthenticationForm,
            })
     
     else:
          user = authenticate(
               request, username = request.POST['username'], password=request.POST['password'])

          if user is None:
                    return render(request, 'logar.html', {
                        'form': AuthenticationForm,
                        "error": 'Usuário ou senha incorretos'
               })

          else:
                    login(request, user)
                    return redirect('crud')
@login_required         
def sair(request):
     logout(request)
     return redirect('home')



def categoria(request, categoria_id=None):
    instance = get_object_or_404(Categoria, id=categoria_id) if categoria_id else None

    if request.method == 'POST':
        if 'nova_categoria' in request.POST:  # Botão "Nova Categoria" clicado
            form = CategoriaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Categoria criada com sucesso!")
                return redirect('categorias')
        else:  # Botão "Salvar" clicado
            form = CategoriaForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, "Categoria atualizada com sucesso!")
                return redirect('categorias')
    else:
        form = CategoriaForm(instance=instance)

    categorias_list = Categoria.objects.all()
    return render(request, 'categorias.html', {'form': form, 'categorias': categorias_list})


def delete_categorias(request):
    if request.method == 'POST':
        selected_categories = request.POST.getlist('selected_categories')
        Categoria.objects.filter(id__in=selected_categories).delete()
        messages.success(request, "Categorias deletadas com sucesso!")
    return redirect('categorias')


def arquivos(request):

    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        if file.name.endswith('.txt'):
            process_txt(file)
        elif file.name.endswith('.xlsx'):
            process_excel(file)
        else:
            messages.error(request, "Tipo de arquivo não suportado!")
        return redirect('crud')
    
def process_txt(file):
    for line in file:
        # Processar cada linha
        (
            nome, email, telefone, cidade, estado, init_contrato, fim_contrato,
            periodicidade, servico, tipo, setor, acoes
        ) = line.decode('utf-8').strip().split(',')
        
        # Limpeza dos campos
        nome = clean_general(nome)
        email = clean_general(email)
        telefone = clean_telefone(telefone)
        cidade = clean_general(cidade)
        estado = clean_general(estado)
        init_contrato = clean_general(init_contrato)
        fim_contrato = clean_general(fim_contrato)
        periodicidade = clean_general(periodicidade)
        servico = clean_general(servico)
        tipo = clean_general(tipo)
        setor = clean_general(setor)
        acoes = clean_general(acoes)
        
        # Verificar ou criar categoria (assumindo que categoria se refere ao setor)
        categoria, _ = Categoria.objects.get_or_create(nome=setor.strip())
        
        # Criar ou atualizar cliente
        cliente, created = Clientes.objects.update_or_create(
            email=email.strip(),
            defaults={
                'nome': nome.strip(),
                'telefone': telefone.strip(),
                'cidade': cidade.strip(),
                'estado': estado.strip(),
                'init_contrato': init_contrato.strip(),
                'fim_contrato': fim_contrato.strip(),
                'periodicidade': periodicidade.strip(),
                'servico': servico.strip(),
                'tipo': tipo.strip(),
                'acoes': acoes.strip(),
            }
        )
        cliente.categoria.add(categoria)



def process_excel(file):
    wb = load_workbook(file)
    sheet = wb.active

    for row in sheet.iter_rows(min_row=2, values_only=True):  # Ignorando o cabeçalho
        (nome, email, telefone, cidade, estado, init_contrato, fim_contrato, 
        periodicidade_nome, servico_nome, tipo_nome, setor, categoria_nome, *rest) = row

        # Processando datas
        if isinstance(init_contrato, datetime):
            init_contrato_date = init_contrato.date()
        elif isinstance(init_contrato, str):
            init_contrato_date = datetime.strptime(init_contrato, '%d/%m/%Y').date()
        else:
            init_contrato_date = None

        if isinstance(fim_contrato, datetime):
            fim_contrato_date = fim_contrato.date()
        elif isinstance(fim_contrato, str):
            fim_contrato_date = datetime.strptime(fim_contrato, '%d/%m/%Y').date()
        else:
            fim_contrato_date = None

        # Verificar ou criar periodicidade, servico e tipo 
        # (Assumindo que esses modelos têm um campo 'nome' para busca)
        periodicidade, _ = Periodicidade.objects.get_or_create(nome=periodicidade_nome)
        servico, _ = Servicos.objects.get_or_create(nome=servico_nome)
        tipo, _ = Tipo.objects.get_or_create(nome=tipo_nome)

        # Verificar ou criar categoria
        categoria_nome = categoria_nome.strip() if categoria_nome else None
        categoria, _ = Categoria.objects.get_or_create(nome=categoria_nome)

        # Criar ou atualizar cliente
        cliente, created = Clientes.objects.update_or_create(
            email=email.strip(),
            defaults={
                'nome': nome.strip(),
                'telefone': int(telefone) if telefone else None,
                'cidade': str(cidade).strip(),
                'estado': estado.strip(),
                'init_contrato': init_contrato_date,
                'fim_contrato': fim_contrato_date,
                'periodicidade': periodicidade,
                'servico': servico,
                'tipo': tipo,
                'setor': setor.strip()
            }
        )
        cliente.categoria.add(categoria)


def clean_telefone(telefone):
    return re.sub(r'\D', '', telefone)  # Remove tudo que não for dígito

def clean_general(field):
    return re.sub(r'[^a-zA-Z0-9@. ]', '', field)

def download_excel(request):
    # Chame a função para gerar o arquivo Excel
    export_to_excel()

    # Abra o arquivo e sirva-o como uma resposta
    with open('clientes.xlsx', 'rb') as excel:
        response = HttpResponse(excel.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=clientes.xlsx'
        return response

def listar_clientes(request):
    # Obter valores únicos dos campos para filtragem
    cidades = Clientes.objects.values_list('cidade', flat=True).distinct()
    estados = Clientes.objects.values_list('estado', flat=True).distinct()
    setores = Clientes.objects.values_list('setor', flat=True).distinct()
    periodicidades = Periodicidade.objects.all()
    servicos = Servicos.objects.all()
    tipos = Tipo.objects.all()
    categorias = Categoria.objects.annotate(num_clients=Count('clientes')).filter(num_clients__gt=0)

    # Inicialmente, não liste nenhum cliente
    clientes = Clientes.objects.none()

    if request.method == 'POST':
        # Aplique os filtros conforme a solicitação POST
        clientes = Clientes.objects.all()
        
        cidade_selecionada = request.POST.get('cidade')
        estado_selecionado = request.POST.get('estado')
        setor_selecionado = request.POST.get('setor')
        tipo_selecionado = request.POST.get('tipo')
        servico_selecionado = request.POST.get('servico')
        periodicidade_selecionada = request.POST.get('periodicidade')
        categoria_selecionada = request.POST.get('categoria')

        if cidade_selecionada:
            clientes = clientes.filter(cidade=cidade_selecionada)
        if estado_selecionado:
            clientes = clientes.filter(estado=estado_selecionado)
        if setor_selecionado:
            clientes = clientes.filter(setor=setor_selecionado)
        if tipo_selecionado:
            clientes = clientes.filter(tipo__id=tipo_selecionado)
        if servico_selecionado:
            clientes = clientes.filter(servico__id=servico_selecionado)
        if periodicidade_selecionada:
            clientes = clientes.filter(periodicidade__id=periodicidade_selecionada)
        if categoria_selecionada:
            clientes = clientes.filter(categoria__id=categoria_selecionada)

    context = {
        'cidades': cidades,
        'estados': estados,
        'setores': setores,
        'tipos': tipos,
        'servicos': servicos,
        'periodicidades': periodicidades,
        'categorias': categorias,
        'clientes': clientes
    }

    return render(request, 'listar_clientes.html', context)


def send_email(request):
    if request.method == 'POST':
        email_subject = request.POST['email_subject']
        email_body_html = request.POST.get('email_body_html', '')
        email_attachment = request.FILES.get('email_attachment', None)
        client_excel_file = request.FILES.get('clientExcelFile', None)

        if client_excel_file is None:
            messages.error(request, "Nenhum arquivo Excel fornecido.")
            return redirect('listar_clientes')

        try:
            excel_file = BytesIO(client_excel_file.read())
            workbook = load_workbook(excel_file)
            first_sheet = workbook.active
            client_emails = []
            client_names = []

            for row in first_sheet.iter_rows(min_row=2):
                email_cell = row[1]  # Assuming emails are in the second column
                name_cell = row[0]  # Assuming names are in the first column
                if email_cell.value and name_cell.value:
                    client_emails.append(email_cell.value)
                    client_names.append(name_cell.value)

        except Exception as e:
            messages.error(request, f"Erro ao ler o arquivo Excel: {str(e)}")
            return redirect('listar_clientes')

        if not client_emails:
            messages.error(request, "A lista de e-mails está vazia.")
            return redirect('listar_clientes')

        smtp_server = 'maladireta.task.com.br'
        smtp_port = 587
        smtp_user = request.POST['email_user']
        smtp_password = request.POST['email_password']

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)

        for email, name in zip(client_emails, client_names):
            personalized_body = email_body_html.replace('{name}', name)
            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = email
            msg['Subject'] = email_subject
            msg.attach(MIMEText(personalized_body, 'html'))

            if email_attachment:
                try:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(email_attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f"attachment; filename= {email_attachment.name}")
                    msg.attach(part)
                except Exception as e:
                    messages.error(request, f"Erro ao anexar arquivo: {str(e)}")
                    return redirect('listar_clientes')

            try:
                server.send_message(msg)
            except Exception as e:
                messages.error(request, f"Erro ao enviar e-mail para {email}: {str(e)}")
                continue  # Continua enviando os próximos e-mails

        server.quit()
        messages.success(request, "Emails enviados com sucesso!")
        return redirect('listar_clientes')

    

def criar_template(request):
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('criar_template')  # Substitua 'some_view_name' pelo nome da view para a qual você deseja redirecionar após salvar. 
    else:
        form = EmailTemplateForm()
    return render(request, 'criar_template.html', {'form': form})

def listar_templates(request):
    templates = EmailTemplate.objects.all()
    return render(request, 'listar_templates.html', {'templates': templates})

def view_template(request, template_id):
    template = get_object_or_404(EmailTemplate, id=template_id)
    return render(request, 'view_template.html', {'template': template})


def edit_template(request, pk):
    template = get_object_or_404(EmailTemplate, id=pk)
    if request.method == "POST":
        form = EmailTemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            return redirect('listar_templates')
    else:
        form = EmailTemplateForm(instance=template)
    return render(request, 'edit_template.html', {'form': form, 'template': template})


def delete_template(request, pk):
    print("Método HTTP:", request.method)
    if request.method == 'POST':
        deleted, _ = EmailTemplate.objects.filter(id=pk).delete()
        if deleted:
            messages.success(request, "Modelo de email deletado com sucesso!")
        else:
            messages.error(request, "Modelo de email não encontrado!")
    else:
        messages.error(request, "Método não permitido!")
    return redirect('listar_templates')


def preview_template(request, template_id):
    template = get_object_or_404(EmailTemplate, id=template_id)
    return render(request, 'preview_template.html', {'template': template})

def get_email_templates(request):
    templates = list(EmailTemplate.objects.values('id', 'subject', 'body'))
    return JsonResponse(templates, safe=False)
