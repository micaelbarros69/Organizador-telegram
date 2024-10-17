from telethon import TelegramClient, events
from config import api_id, api_hash, bot_token, caminho
from message_handler import processar_mensagem
from ocr_utils import processar_imagem, processar_pdf

# Iniciar o cliente Telegram
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Função para capturar novas mensagens
@client.on(events.NewMessage)
async def handler(event):
    # Verificar se a mensagem contém texto
    message_text = event.message.message
    if message_text:
        await processar_mensagem(message_text)
    
    # Verificar se a mensagem contém mídia (fotos ou PDFs)
    if event.message.media:
        # Baixar o arquivo anexado
        media_path = await event.message.download_media(file=f'./Downloads/{event.message.file.name}')
        print(f"Arquivo recebido e salvo em: {media_path}")

        # Verificar se o arquivo é um PDF
        if media_path.endswith('.pdf'):
            print("Arquivo PDF detectado.")
            processar_pdf(media_path)  # Chama a função para processar PDFs
        elif media_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            print("Imagem detectada.")
            await processar_imagem(event)  # Chama a função para processar imagens
        else:
            print("Tipo de arquivo não suportado.")

# Rodar o bot
print("Bot em execução...")
client.run_until_disconnected()
