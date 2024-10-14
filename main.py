from telethon import TelegramClient, events
import re
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import os
import openpyxl
import cv2
import numpy as np 

# Configuração do caminho do Tesseract no seu sistema (no Windows, por exemplo)
caminho = r'C:\Program Files\Tesseract-OCR'

# Substitua com suas credenciais reais
api_id = '28768988'  # O api_id deve ser numérico
api_hash = '33d890e08de6d6d69d5abcd9488002aa'
bot_token = '8115583628:AAHQeVBLaXOXq_pwUPixEIDmj0cj5V0ctQ4'

# Iniciar o cliente Telegram
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Função para salvar dados no Excel
def salvar_dados_no_excel(dados):
    caminho_planilha = 'retornos.xlsx'
    
    # Tentar abrir o arquivo ou criar um novo
    try:
        wb = openpyxl.load_workbook(caminho_planilha)
        sheet = wb.active
    except FileNotFoundError:
        wb = openpyxl.Workbook()
        sheet = wb.active
        # Adicionar cabeçalhos
        sheet.append(['ID', 'Projeto', 'Data', 'Local', 'Observações'])
    
    # Adicionar os dados extraídos
    sheet.append(dados)
    
    # Salvar a planilha
    wb.save(caminho_planilha)

# Função para capturar mensagens
@client.on(events.NewMessage)
async def handler(event):
    # Extrair a mensagem de texto
    message_text = event.message.message
    if message_text:
        print(f"Mensagem recebida: {message_text}")

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
        
        # Salvar no Excel
        salvar_dados_no_excel([id_projeto, num_projeto, data, local, observacoes])


# Função para capturar mensagens
@client.on(events.NewMessage)
async def handler(event):
    # Extrair a mensagem de texto
    message_text = event.message.message
    if message_text:
        print(f"Mensagem recebida: {message_text}")

    # Verificar se a mensagem contém fotos
    if event.message.media:
        # Baixar a foto anexada
        photo_path = await event.message.download_media(file=f'./Fotos/Foto_{event.message.id}.jpg')
        print(f"Foto salva em: {photo_path}")

        # Ler o texto da foto usando OCR com pré-processamento
        pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"

        # Abrir a imagem
        image = Image.open(photo_path)

                # Pré-processamento mais agressivo
        gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        # Converter para escala de cinza
        image = image.convert('L')

        # # # # Ler o texto da imagem após o pré-processamento
        text_in_image = pytesseract.image_to_string(image, config='--oem 3 --psm 6')
        print(f"Texto extraído da imagem (após pré-processamento): {text_in_image}")

        # Procurar pela ID no texto da imagem
        match = re.search(r'INC: (\d+)', text_in_image)
        if match:
            id_number = match.group(1)
            print(f"ID encontrada na imagem: {id_number}")

            # Criar uma pasta para a ID se não existir
            id_folder = f'./Fotos/{id_number}'
            if not os.path.exists(id_folder):
                os.makedirs(id_folder)
            
            # Mover a foto para a pasta correspondente
            os.rename(photo_path, f'{id_folder}/Foto_{event.message.id}.jpg')
            print(f"Foto movida para a pasta: {id_folder}/Foto_{event.message.id}.jpg")

# Rodar o bot
print("Bot em execução...")
client.run_until_disconnected()
