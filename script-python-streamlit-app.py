import streamlit as st
from storage import upload_to_blob
from ai_service import analyze_credit_card

def show_image_and_validation(blob_url, credit_card_info):
    st.image(blob_url, caption="Imagem analisada", use_column_width=True)
    st.write("---")
    st.write("### Resultado da Validação:")
    
    # Valida se a IA conseguiu extrair pelo menos o nome (indicando que leu um cartão)
    if credit_card_info and credit_card_info.get("card_name"):
        st.markdown("<h1 style='color: green;'>✅ Cartão Válido</h1>", unsafe_allow_html=True)
        st.write(f"**Nome do Titular:** {credit_card_info.get('card_name', 'Não identificado')}")
        st.write(f"**Banco Emissor:** {credit_card_info.get('bank_name', 'Não identificado')}")
        st.write(f"**Data de Validade:** {credit_card_info.get('expiry_date', 'Não identificado')}")
    else:
        st.markdown("<h1 style='color: red;'>❌ Cartão Inválido</h1>", unsafe_allow_html=True)
        st.write("Não foi possível validar este documento. Certifique-se de que é um cartão de crédito legível.")

def configure_interface():
    st.title("Upload de Arquivo DIO - Desafio 1 - Azure")
    st.write("Envie a foto de um cartão de crédito para validação anti-fraude.")
    
    uploaded_file = st.file_uploader("Escolha um arquivo", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        file_name = uploaded_file.name
        
        # 1. Manda para o Blob Storage com um "spinner" visual de carregamento
        with st.spinner("☁️ Enviando imagem para o Azure Storage..."):
            blob_url = upload_to_blob(uploaded_file, file_name)
        
        if blob_url:
            st.success(f"Arquivo enviado com sucesso!")
            
            # 2. Chama a IA do Document Intelligence com outro "spinner"
            with st.spinner("🤖 Analisando documento com Inteligência Artificial..."):
                credit_card_info = analyze_credit_card(blob_url)
            
            # 3. Mostra o resultado na tela
            show_image_and_validation(blob_url, credit_card_info)
        else:
            st.error("Erro ao enviar a imagem para o Azure. Verifique o terminal para mais detalhes.")

if __name__ == "__main__":
    configure_interface()
