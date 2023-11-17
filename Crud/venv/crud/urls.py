from django.contrib import admin
from django.urls import path, include
from app.views import crud, form, create, view, edit, update, delete
from app.views import home, cadastro, logar, sair, listar_clientes, categoria, delete_categorias, arquivos, download_excel, send_email, criar_template, listar_templates, view_template, edit_template, delete_template, preview_template, get_email_templates
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('django.contrib.auth.urls')),
    path('crud/', crud, name= 'crud'),
    path('form/', form, name= 'form'),
    path('create/', create, name= 'create'),
    path('view/<int:pk>/', view, name= 'view'),
    path('edit/<int:pk>/', edit, name= 'edit'),
    path('update/<int:pk>/', update, name= 'update'),
    path('delete/<int:pk>/', delete, name= 'delete'),
    path('', home, name='home'),
    path('cadastro/', cadastro, name='cadastro'),
    path('logar/', logar, name='logar'),
    path('sair/', sair, name='sair'),
    path('clientes/', listar_clientes, name='listar_clientes'),
    path('categorias/', categoria, name='categorias'),
    path('categorias/<int:categoria_id>/', categoria, name='edit_categoria'),
    path('categorias/delete/', delete_categorias, name='delete_categorias'),
    path('arquivos/', arquivos, name='arquivos'),
    path('download_excel/', download_excel, name='download_excel'),
    path('listar_clientes/', listar_clientes, name='listar_clientes'),
    path('send_email/', send_email, name='send_email'),
    path('criar_template/', criar_template, name='criar_template'),
    path('listar_templates/', listar_templates, name='listar_templates'),
    path('visualizar-modelo/<int:template_id>/', view_template, name='view_template'),
    path('template/edit/<int:pk>/', edit_template, name='edit_template'),
    path('template/delete/<int:pk>/', delete_template, name='delete_template'),
    path('preview-modelo/<int:template_id>/', preview_template, name='preview_template'),
    path('get_email_templates/', get_email_templates, name='get_email_templates'),

]
