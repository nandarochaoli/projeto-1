import streamlit as st
import re

# =========================================================================
# FUNÇÕES DE BUSCA (Lógica)
# =========================================================================

def formatar_artigo(texto_artigo):
    """Pega os primeiros 300 caracteres do artigo para dar um 'preview'."""
    # NOVIDADE: Limite do preview aumentado para 300 caracteres.
    LIMITE_PREVIEW = 300 
    
    preview = texto_artigo.strip()
    
    if len(preview) > LIMITE_PREVIEW:
        preview = preview[:LIMITE_PREVIEW] + "..."
    
    return preview

def buscar_em_arquivo(termo_pesquisa, nome_arquivo):
    """
    Função principal que busca um termo em um arquivo de texto.
    Retorna uma lista de strings com os resultados.
    """
    encontrados = []
    
    if not termo_pesquisa:
        return []

    try:
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
        encontrados.append(f"🚨 ERRO: O arquivo '{nome_arquivo}' não foi encontrado!")
    
    return encontrados

# =========================================================================
# ESTRUTURA DO APLICATIVO STREAMLIT (Com Apresentação Vertical)
# =========================================================================

# Título e cabeçalho da página
st.title("🏛️ Buscador Jurídico Rápido")
st.subheader("Constituição Federal e Código Civil")

# 1. Interação do Usuário
termo_pesquisa = st.text_input(
    "Digite a palavra ou expressão exata que deseja buscar:",
    placeholder="Ex: dignidade da pessoa humana"
)

# 2. Execução da Lógica: A busca só ocorre se o usuário digitar algo
if termo_pesquisa:
 # --- Busca na Constituição ---
st.markdown("---") # Separador visual
st.header("1. Constituição Federal")

# Chama a função de busca
resultados_cf = buscar_em_arquivo(termo_pesquisa, "constituicao.txt")

# A CORREÇÃO ESTÁ AQUI:
# 1. Primeiro verificamos se a lista não está vazia (len(resultados_cf) > 0)
# 2. Depois verificamos se a primeira entrada contém a palavra "ERRO".

if len(resultados_cf) > 0 and "ERRO" in resultados_cf[0]:
    # Trata o caso de erro de arquivo
    st.error(resultados_cf[0]) 
elif len(resultados_cf) > 0:
    # Trata o caso de sucesso
    st.success(f"✅ Termo encontrado em {len(resultados_cf)} Artigos da CF:")
    for resultado in resultados_cf:
        st.markdown(resultado)
else:
    # Trata o caso da lista vazia (termo não encontrado)
    st.info(f"❌ Termo '{termo_pesquisa}' não encontrado na Constituição Federal.")

# --- Busca no Código Civil ---

st.markdown("---") # Separador visual
st.header("2. Código Civil")

# Chama a função de busca
resultados_cc = buscar_em_arquivo(termo_pesquisa, "codigo_civil.txt")

# Aplicando a mesma correção ao Código Civil
if len(resultados_cc) > 0 and "ERRO" in resultados_cc[0]:
    # Trata o caso de erro de arquivo
    st.error(resultados_cc[0])
elif len(resultados_cc) > 0:
    # Trata o caso de sucesso
    st.success(f"✅ Termo encontrado em {len(resultados_cc)} Artigos do Código Civil:")
    for resultado in resultados_cc:
        st.markdown(resultado)
else:
    # Trata o caso da lista vazia (termo não encontrado)
    st.info(f"❌ Termo '{termo_pesquisa}' não encontrado no Código Civil.")

st.markdown("---")
