import re
from excel_utils import salvar_dados_no_excel


async def processar_mensagem(message_text):
    # Usar regex para capturar ID, Projeto, Data, Local e Observações
    padrao_id = r"ID:\s*(-?\d+)"
    padrao_projeto = r"Projeto:\s*(\d+)"
    padrao_data = r"Data:\s*([\d/]+)"
    padrao_local = r"Local:\s*(.*)"
    padrao_observacoes = r"Observações:\s*(.*)"
    
    # Capturar ID, Projeto, Data, Local e Observações (se existir)
    id_projeto = re.search(padrao_id, message_text)
    num_projeto = re.search(padrao_projeto, message_text)
    data = re.search(padrao_data, message_text)
    local = re.search(padrao_local, message_text)
    observacoes = re.search(padrao_observacoes, message_text)

    # Verificar e preencher com "N/A" se algum campo estiver faltando
    id_projeto = id_projeto.group(1) if id_projeto else "N/A"
    num_projeto = num_projeto.group(1) if num_projeto else "N/A"
    data = data.group(1) if data else "N/A"
    local = local.group(1) if local else "N/A"
    observacoes = observacoes.group(1) if observacoes else "N/A"

    print(f"ID: {id_projeto}, Projeto: {num_projeto}, Data: {data}, Local: {local}, Observações: {observacoes}")
    
    # Salvar os dados no Excel
    salvar_dados_no_excel([id_projeto, num_projeto, data, local, observacoes])
    
