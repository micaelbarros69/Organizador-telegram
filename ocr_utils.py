import os
from google.cloud import vision
import io
import re
from pdf2image import convert_from_path

# Configuração do caminho do JSON da Google Cloud Vision API (se ainda não configurou a variável de ambiente)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:/Users/User/Desktop/Programação PY/AUTOMAÇÃO DO TELEGRAM/chave/credencial.json'



async def processar_imagem(event):
    photo_path = await event.message.download_media(file=f'./Fotos/Foto_{event.message.id}.jpg')
    print(f"Foto salva em: {photo_path}")
    

    # Função para usar o Google Cloud Vision para extrair texto
    def detect_text_google_cloud(image_path):
        """Detecta texto em uma imagem usando Google Cloud Vision API."""
        client = vision.ImageAnnotatorClient()

        # Abre a imagem
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        # Chama a API para detectar o texto
        response = client.text_detection(image=image)
        texts = response.text_annotations

        if texts:
            print(f"Texto detectado")
            return texts[0].description
        else:
            print("Nenhum texto detectado.")
            return ""

        if response.error.message:
            raise Exception(f'Erro da API: {response.error.message}')

    # Chamar a função que usa o Google Cloud Vision API para extrair o texto da imagem
    text_in_image = detect_text_google_cloud(photo_path)
    print(f"Texto extraído da imagem: {text_in_image}")

    # Melhorar a busca pela ID, agora aceitando números negativos
    pattern = r'ID\s*[: ]\s*(-?\d+)'  # Ajustado para incluir números negativos
    match = re.search(pattern, text_in_image)   

    if match:
        id_number = match.group(1)
        print(f"ID encontrada na imagem: {id_number}")

        # Criar uma pasta para a ID se não existir
        id_folder = f'./Fotos/{id_number}'
        if not os.path.exists(id_folder):
            os.makedirs(id_folder)

        # Mover a foto para a pasta correspondente
        new_photo_path = f'{id_folder}/Foto_{event.message.id}.jpg'
        os.rename(photo_path, new_photo_path)
        print(f"Foto movida para a pasta: {new_photo_path}")
    else:
        print("ID não encontrada no texto extraído.")

# Função para processar um arquivo PDF
def processar_pdf(pdf_path):
    # Converte o PDF em uma lista de imagens
    pages = convert_from_path(pdf_path, 300)  # 300 DPI para garantir boa qualidade
    
    for page_number, image in enumerate(pages, start=1):
        # Salva cada página como uma imagem temporária
        image_path = f'./Fotos/pagina_{page_number}.jpg'
        image.save(image_path, 'JPEG')
        
        # Chama a função de detecção de texto em cada imagem
        texto_extraido = detect_text_google_cloud(image_path)
        print(f"Texto extraído da página {page_number}: {texto_extraido}")
        
        # Aqui você pode continuar o processo de extração e salvar em planilha conforme seu código original

# Função para usar o Google Cloud Vision para extrair texto de imagens
def detect_text_google_cloud(image_path):
    """Detecta texto em uma imagem usando Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()

    # Abre a imagem
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Chama a API para detectar o texto
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description
    else:
        return ""

    if response.error.message:
        raise Exception(f'Erro da API: {response.error.message}')