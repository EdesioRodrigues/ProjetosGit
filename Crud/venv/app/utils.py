import pandas as pd
from app.models import Clientes, Categoria, Tipo, Periodicidade, Servicos

def export_to_excel():
    # Obtenha todos os registros do modelo Clientes
    clientes = Clientes.objects.all()

    # Crie uma lista para armazenar os dados
    data = []

    # Itere sobre cada cliente e extraia os dados necessários
    for cliente in clientes:
        data.append({
            'Nome': cliente.nome,
            'Email': cliente.email,
            'Telefone': cliente.telefone,
            'Cidade': cliente.cidade,
            'Estado': cliente.estado,
            'Início do Contrato': cliente.init_contrato,
            'Fim do Contrato': cliente.fim_contrato,
            'Periodicidade': str(cliente.periodicidade),
            'Serviço': str(cliente.servico),
            'Tipo': str(cliente.tipo),
            'Setor': cliente.setor,
            'Categorias': ', '.join([str(cat) for cat in cliente.categoria.all()]),
        })

    # Converta a lista de dados em um DataFrame do pandas
    df = pd.DataFrame(data)

    # Salve o DataFrame em um arquivo Excel
    df.to_excel('clientes.xlsx', index=False)
