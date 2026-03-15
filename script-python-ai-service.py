import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from dotenv import load_dotenv

load_dotenv()

def analyze_credit_card(blob_url):
    try:
        endpoint = os.getenv("AZURE_DI_ENDPOINT")
        key = os.getenv("AZURE_DI_KEY")
        
        # Inicia o cliente do Document Intelligence
        document_client = DocumentAnalysisClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )
        
        # Manda analisar a imagem pela URL
        poller = document_client.begin_analyze_document_from_url("prebuilt-document", blob_url)
        result = poller.result()
        
        card_info = {}
        
        # Percorre os pares de texto que a IA encontrou para montar nosso dicionário
        for kv_pair in result.key_value_pairs:
            if kv_pair.key and kv_pair.value:
                key_text = kv_pair.key.content.lower()
                value_text = kv_pair.value.content
                
                # Lógica básica para identificar os campos (pode ser ajustada dependendo dos cartões fake)
                if "name" in key_text or "nome" in key_text:
                    card_info["card_name"] = value_text
                elif "bank" in key_text or "banco" in key_text:
                    card_info["bank_name"] = value_text
                elif "valid" in key_text or "exp" in key_text or "date" in key_text:
                    card_info["expiry_date"] = value_text
        
        return card_info
        
    except Exception as e:
        print(f"Erro na análise de Document Intelligence: {e}")
        return None
