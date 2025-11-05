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
            # Permite a captura de números de artigo com pontos (ex: Art. 1.762)
            # =================================================================
            artigos = re.split(r'(\sArt\.\s[\d\.]+)', conteudo_completo)

            for i in range(1, len(artigos), 2):
                numero_artigo = artigos[i].strip()
                texto_do_artigo = artigos[i+1]

                # A busca é feita de forma case-insensitive
                if termo_pesquisa.lower() in texto_do_artigo.lower():
                    preview = formatar_artigo(texto_do_artigo)
                    
                    # Formato normal (corpo de texto) sem caixas suspensas
                    resultado_formatado = f"**{numero_artigo}:** {preview}"
                    
                    encontrados.append(resultado_formatado)
                    
    except FileNotFoundError:
        # Mensagem de erro que será detectada no bloco principal
        encontrados.append(f"🚨 ERRO: O arquivo '{nome_arquivo}' não foi encontrado!")
    
    return encontrados

# =========================================================================
# ESTRUTURA DO APLICATIVO STREAMLIT (Uma única vez)
# =========================================================================

# Título e cabeçalho da página
st.title("🏛️ Buscador Jurídico Rápido")
# 1. SUBTÍTULO ATUALIZADO
st.subheader("A ferramenta tem como base: CF/88, CC/02, CP/40 , CPP/41, CDC/90 atualizados até o dia 05/11/2025.")

# 1. Interação do Usuário
termo_pesquisa = st.text_input(
    "Digite a palavra ou expressão exata que deseja buscar:",
    placeholder="Ex: dignidade da pessoa humana"
)


# 2. Execução da Lógica: A busca só ocorre se o usuário digitar algo
if termo_pesquisa:
    
    # ------------------ INÍCIO DO BLOCO INDENTADO ------------------
    
    # 2. BOTÕES DE NAVEGAÇÃO RÁPIDA (Agora só aparecem com o termo de pesquisa)
    st.markdown("---")
    st.markdown("### Navegação Rápida (Clique para rolar até a seção)")
    
    # Layout dos botões em colunas para melhor visualização
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("[🇧🇷 CF](#cf_anchor)", unsafe_allow_html=True)
    with col2:
        st.markdown("[🤵 CC](#cc_anchor)", unsafe_allow_html=True)
    with col3:
        st.markdown("[🚨 CP](#cp_anchor)", unsafe_allow_html=True)
    with col4:
        st.markdown("[⚖️ CPP](#cpp_anchor)", unsafe_allow_html=True)
    with col5:
        st.markdown("[🛍️ CDC](#cdc_anchor)", unsafe_allow_html=True)

    st.markdown("---")

    # --- Busca na Constituição ---
    st.markdown("---") # Separador visual
    # ÂNCORA HTML INSERIDA PARA NAVEGAÇÃO
    st.markdown('<a name="cf_anchor"></a>', unsafe_allow_html=True)
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
    # ÂNCORA HTML INSERIDA PARA NAVEGAÇÃO
    st.markdown('<a name="cc_anchor"></a>', unsafe_allow_html=True)
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
    # ÂNCORA HTML INSERIDA PARA NAVEGAÇÃO
    st.markdown('<a name="cp_anchor"></a>', unsafe_allow_html=True)
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
    # ÂNCORA HTML INSERIDA PARA NAVEGAÇÃO
    st.markdown('<a name="cdc_anchor"></a>', unsafe_allow_html=True)
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
    

    # --- Busca no Código de Processo Penal ---
    
    st.markdown("---") # Separador visual
    # ÂNCORA HTML INSERIDA PARA NAVEGAÇÃO
    st.markdown('<a name="cpp_anchor"></a>', unsafe_allow_html=True)
    st.header("5. Código de Processo Penal")

    # Chama a função de busca
    resultados_cpp = buscar_em_arquivo(termo_pesquisa, "codigo_processo_penal.txt")
    
    # Tratamento do Código de Processo Penal (CPP)
    if len(resultados_cpp) > 0 and "ERRO" in resultados_cpp[0]:
        st.error(resultados_cpp[0])
    elif len(resultados_cpp) > 0:
        st.success(f"✅ Termo encontrado em {len(resultados_cpp)} Artigos do Código de Processo Penal:")
        for resultado in resultados_cpp:
            st.markdown(resultado)
    else:
        st.info(f"❌ Termo '{termo_pesquisa}' não encontrado no Código de Processo Penal.")

    
    st.markdown("---")
    # ------------------ FIM DO BLOCO INDENTADO ------------------
