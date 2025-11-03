import streamlit as st
import re



def formatar_artigo(texto_artigo):
    """Pega os primeiros 150 caracteres do artigo para dar um 'preview'."""
    preview = texto_artigo.strip()
    
    if len(preview) > 150:
        preview = preview[:150] + "..."
    
    return preview

def buscar_em_arquivo(termo_pesquisa, nome_arquivo):
    """
    Função principal que busca um termo em um arquivo de texto.
    Retorna uma lista de strings com os resultados.
    """
    encontrados = []
    
    # Verifica se o termo de pesquisa é válido antes de abrir o arquivo
    if not termo_pesquisa:
        return []

    try:
        # 'utf-8-sig' ajuda a ignorar caracteres 'estranhos' que podem vir da web
        with open(nome_arquivo, 'r', encoding='utf-8-sig') as f:
            conteudo_completo = f.read()
            
            # A lógica de divisão por artigo continua a mesma
            artigos = re.split(r'(\sArt\.\s\d+)', conteudo_completo)

            for i in range(1, len(artigos), 2):
                numero_artigo = artigos[i].strip()
                texto_do_artigo = artigos[i+1]

                # A busca é feita de forma case-insensitive
                if termo_pesquisa.lower() in texto_do_artigo.lower():
                    preview = formatar_artigo(texto_do_artigo)
                    
                    # Formata o resultado em Markdown para exibição no Streamlit
                    resultado_formatado = f"**{numero_artigo}º:** *{preview}*"
                    encontrados.append(resultado_formatado)
                    
    except FileNotFoundError:
        # Se o arquivo não for encontrado, retorna uma mensagem de erro
        encontrados.append(f"🚨 ERRO: O arquivo '{nome_arquivo}' não foi encontrado!")
    
    return encontrados

# =========================================================================
# ESTRUTURA DO APLICATIVO STREAMLIT
# =========================================================================

# Título e cabeçalho da página
st.title("🏛️ Google Jurídico")
st.subheader("Constituição Federal, Código Civil")

# 1. Interação do Usuário: st.text_input(
    "Digite a palavra ou expressão exata que deseja buscar:",
    placeholder="Ex: dignidade da pessoa humana"
)

# 2. Execução da Lógica: A busca só ocorre se o usuário digitar algo
if termo_pesquisa:


    # --- Busca na Constituição ---
    with col1:
        st.header("Constituição Federal")
        
        # Chama a função de busca
        resultados_cf = buscar_em_arquivo(termo_pesquisa, "constituicao.txt")

        if resultados_cf and "ERRO" not in resultados_cf[0]:
            st.success(f"✅ Encontrado em {len(resultados_cf)} Artigos:")
            # 3. Saída de Informação: Usamos st.markdown no lugar de print()
            for resultado in resultados_cf:
                st.markdown(resultado)
        elif "ERRO" in resultados_cf[0]:
             st.error(resultados_cf[0])
        else:
            st.info(f"❌ Termo '{termo_pesquisa}' não encontrado na CF.")

    # --- Busca no Código Civil ---
    with col2:
        st.header("Código Civil")

        # Chama a função de busca
        resultados_cc = buscar_em_arquivo(termo_pesquisa, "codigo_civil.txt")
        
        if resultados_cc and "ERRO" not in resultados_cc[0]:
            st.success(f"✅ Encontrado em {len(resultados_cc)} Artigos:")
            for resultado in resultados_cc:
                st.markdown(resultado)
        elif "ERRO" in resultados_cc[0]:
             st.error(resultados_cc[0])
        else:
            st.info(f"❌ Termo '{termo_pesquisa}' não encontrado no CC.")
