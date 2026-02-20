import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

def upload_to_blob(file, file_name):
    try:
        # Puxa a string de conexão do arquivo .env
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        container_name = "cartoes" # ⚠️ Lembre-se de criar esse container no seu Storage Account!
        
        # Conecta no serviço
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
        
        # Faz o upload do arquivo
        blob_client.upload_blob(file, overwrite=True)
        
        # Retorna a URL pública do arquivo
        return blob_client.url
    except Exception as e:
        print(f"Erro no upload para o Blob Storage: {e}")
        return None
