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
            
            # =================================================================
            # CORREÇÃO APLICADA AQUI:
            # Trocamos \d+ (apenas dígitos) por [\d\.]+ (dígitos E pontos).
            # Isso permite que a regex capture "Art. 1.762" corretamente.
            # =================================================================
            artigos = re.split(r'(\sArt\.\s[\d\.]+)', conteudo_completo)

            for i in range(1, len(artigos), 2):
                numero_artigo = artigos[i].strip()
                texto_do_artigo = artigos[i+1]

                # A busca é feita de forma case-insensitive
                if termo_pesquisa.lower() in texto_do_artigo.lower():
                    preview = formatar_artigo(texto_do_artigo)
                    
                    # Formata o resultado em Markdown para exibição no Streamlit
                    resultado_formatado = f"**{numero_artigo}:** {preview}"
                    encontrados.append(resultado_formatado)
                    
    except FileNotFoundError:
        # Mensagem de erro que será detectada no bloco principal
        encontrados.append(f"🚨 ERRO: O arquivo '{nome_arquivo}' não foi encontrado!")
    
    return encontrados

# =========================================================================
# ESTRUTURA DO APLICATIVO STREAMLIT (Sem alterações)
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

      # --- Busca no Código Penal ---
    
    st.markdown("---") # Separador visual
    st.header("3. Código Penal")

    # Chama a função de busca
    resultados_cc = buscar_em_arquivo(termo_pesquisa, "codigo_penal.txt")
    
    # Tratamento do Código Penal (CP)
    if len(resultados_cc) > 0 and "ERRO" in resultados_cc[0]:
        st.error(resultados_cc[0])
    elif len(resultados_cc) > 0:
        st.success(f"✅ Termo encontrado em {len(resultados_cc)} Artigos do Código Penal:")
        for resultado in resultados_cc:
            st.markdown(resultado)
    else:
        st.info(f"❌ Termo '{termo_pesquisa}' não encontrado no Código Penal.")

  # --- Busca no Código de Defesa do Consumidor ---
    
    st.markdown("---") # Separador visual
    st.header("4. Código de Defesa do Consumidor")

    # Chama a função de busca
    resultados_cc = buscar_em_arquivo(termo_pesquisa, "codigo_defesa_consumidor.txt")
    
    # Tratamento do Código de Defesa do Consumidor (CDC)
    if len(resultados_cc) > 0 and "ERRO" in resultados_cc[0]:
        st.error(resultados_cc[0])
    elif len(resultados_cc) > 0:
        st.success(f"✅ Termo encontrado em {len(resultados_cc)} Artigos do Código de Defesa do Consumidor:")
        for resultado in resultados_cc:
            st.markdown(resultado)
    else:
        st.info(f"❌ Termo '{termo_pesquisa}' não encontrado no Código de Defesa do Consumidor.")
    
    st.markdown("---")
    # ------------------ FIM DO BLOCO INDENTADO ------------------

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
            
            # =================================================================
            # CORREÇÃO APLICADA AQUI:
            # Trocamos \d+ (apenas dígitos) por [\d\.]+ (dígitos E pontos).
            # Isso permite que a regex capture "Art. 1.762" corretamente.
            # =================================================================
            artigos = re.split(r'(\sArt\.\s[\d\.]+)', conteudo_completo)

            for i in range(1, len(artigos), 2):
                numero_artigo = artigos[i].strip()
                texto_do_artigo = artigos[i+1]

                # A busca é feita de forma case-insensitive
                if termo_pesquisa.lower() in texto_do_artigo.lower():
                    preview = formatar_artigo(texto_do_artigo)
                    
                    # Formata o resultado em Markdown para exibição no Streamlit
                    resultado_formatado = f"**{numero_artigo}:** {preview}"
                    encontrados.append(resultado_formatado)
                    
    except FileNotFoundError:
        # Mensagem de erro que será detectada no bloco principal
        encontrados.append(f"🚨 ERRO: O arquivo '{nome_arquivo}' não foi encontrado!")
    
    return encontrados

# =========================================================================
# ESTRUTURA DO APLICATIVO STREAMLIT (Sem alterações)
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

      # --- Busca no Código Penal ---
    
    st.markdown("---") # Separador visual
    st.header("3. Código Penal")

    # Chama a função de busca
    resultados_cp = buscar_em_arquivo(termo_pesquisa, "codigo_penal.txt")
    
    # Tratamento do Código Penal (CP)
    if len(resultados_cp) > 0 and "ERRO" in resultados_cp[0]:
        st.error(resultados_cp[0])
    elif len(resultados_cp) > 0:
        st.success(f"✅ Termo encontrado em {len(resultados_cp)} Artigos do Código Penal:")
        for resultado in resultados_cp:
            st.markdown(resultado)
    else:
        st.info(f"❌ Termo '{termo_pesquisa}' não encontrado no Código Penal.")

  # --- Busca no Código de Defesa do Consumidor ---
    
    st.markdown("---") # Separador visual
    st.header("4. Código de Defesa do Consumidor")

    # Chama a função de busca
    resultados_cdc = buscar_em_arquivo(termo_pesquisa, "codigo_defesa_consumidor.txt")
    
    # Tratamento do Código de Defesa do Consumidor (CDC)
    if len(resultados_cdc) > 0 and "ERRO" in resultados_cdc[0]:
        st.error(resultados_cdc[0])
    elif len(resultados_cdc) > 0:
        st.success(f"✅ Termo encontrado em {len(resultados_cdc)} Artigos do Código de Defesa do Consumidor:")
        for resultado in resultados_cdc:
            st.markdown(resultado)
    else:
        st.info(f"❌ Termo '{termo_pesquisa}' não encontrado no Código de Defesa do Consumidor.")
    
    st.markdown("---")
    # ------------------ FIM DO BLOCO INDENTADO ------------------



