import streamlit as st
import re

# =========================================================================
# FUNÇÕES DE BUSCA (Lógica)
# =========================================================================

def formatar_artigo(texto_artigo):
    """Pega os primeiros 300 caracteres do artigo para dar um 'preview'."""
    # Limite do preview aumentado para 300 caracteres.
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
            
            # NOVO CÓDIGO AQUI: Expressão regular mais robusta
            # Ela busca por "Art. [número]" de forma mais isolada
            # O padrão (Art.\s\d+) captura o número completo do artigo
            artigos = re.split(r'(?i)(?:\s|\n)(Art\.\s\d+)', conteudo_completo)

            # A lógica de iteração se mantém, mas agora o índice 1 deve ser mais confiável
            # O primeiro item é o texto antes do primeiro artigo (Preâmbulo, Título, etc.)
            for i in range(1, len(artigos), 2):
                
                # O número do artigo (Ex: "Art. 1" ou "Art. 1193")
                numero_artigo = artigos[i].strip() 
                
                # O texto que vem logo depois do número do artigo
                texto_do_artigo = artigos[i+1] 

                # A busca é feita de forma case-insensitive
                if termo_pesquisa.lower() in texto_do_artigo.lower():
                    preview = formatar_artigo(texto_do_artigo)
                    
                    # Remove o "Art." se ele vier no texto (já temos ele no numero_artigo)
                    if texto_do_artigo.strip().startswith(numero_artigo):
                        texto_do_artigo = texto_do_artigo.strip()[len(numero_artigo):]

                    # Formata o resultado em Markdown para exibição no Streamlit
                    # Usamos 'numero_artigo' diretamente, sem o 'º' extra
                    resultado_formatado = f"**{numero_artigo}º:** *{preview}*"
                    encontrados.append(resultado_formatado)
                    
    except FileNotFoundError:
        encontrados.append(f"🚨 ERRO: O arquivo '{nome_arquivo}' não foi encontrado!")
    
    return encontrados


# =========================================================================
# ESTRUTURA DO APLICATIVO STREAMLIT (CORRIGIDO)
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
    
    # ------------------ INÍCIO DO BLOCO INDENTADO ------------------
    
    # --- Busca na Constituição ---
    st.markdown("---") # Separador visual
    st.header("1. Constituição Federal")
    
    # Chama a função de busca
    resultados_cf = buscar_em_arquivo(termo_pesquisa, "constituicao.txt")

    # Tratamento da Constituição Federal (CF)
    if len(resultados_cf) > 0 and "ERRO" in resultados_cf[0]:
        st.error(resultados_cf[0]) 
    elif len(resultados_cf) > 0:
        st.success(f"✅ Termo encontrado em {len(resultados_cf)} Artigos da CF:")
        for resultado in resultados_cf:
            st.markdown(resultado)
    else:
        st.info(f"❌ Termo '{termo_pesquisa}' não encontrado na Constituição Federal.")

    # --- Busca no Código Civil ---
    
    st.markdown("---") # Separador visual
    st.header("2. Código Civil")

    # Chama a função de busca
    resultados_cc = buscar_em_arquivo(termo_pesquisa, "codigo_civil.txt")
    
    # Tratamento do Código Civil (CC)
    if len(resultados_cc) > 0 and "ERRO" in resultados_cc[0]:
        st.error(resultados_cc[0])
    elif len(resultados_cc) > 0:
        st.success(f"✅ Termo encontrado em {len(resultados_cc)} Artigos do Código Civil:")
        for resultado in resultados_cc:
            st.markdown(resultado)
    else:
        st.info(f"❌ Termo '{termo_pesquisa}' não encontrado no Código Civil.")

    st.markdown("---")
    # ------------------ FIM DO BLOCO INDENTADO ------------------
