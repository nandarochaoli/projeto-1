streamlit run app.py
import streamlit as st
import json
import difflib
from typing import List, Dict

# =====================================================
# SIMULAÇÃO DE BASE DE DADOS (você depois substituirá pela API real)
# =====================================================
# Cada código é um dicionário com artigos e textos.
# Você pode carregar isso via API pública no futuro.
CODES = {
    "Constituição Federal": {
        "Lei": "Constituição da República Federativa do Brasil de 1988",
        "Artigos": {
            "5º": "Todos são iguais perante a lei, sem distinção de qualquer natureza...",
            "37": "A administração pública direta e indireta de qualquer dos Poderes..."
        }
    },
    "Código Civil": {
        "Lei": "Lei nº 10.406, de 10 de janeiro de 2002",
        "Artigos": {
            "186": "Aquele que, por ação ou omissão voluntária, negligência ou imprudência, violar direito e causar dano a outrem...",
            "927": "Aquele que, por ato ilícito, causar dano a outrem, fica obrigado a repará-lo."
        }
    },
    "Código Penal": {
        "Lei": "Decreto-Lei nº 2.848, de 7 de dezembro de 1940",
        "Artigos": {
            "121": "Matar alguém: Pena - reclusão, de seis a vinte anos.",
            "129": "Ofender a integridade corporal ou a saúde de outrem..."
        }
    }
}

# =====================================================
# FUNÇÕES AUXILIARES
# =====================================================

def buscar_artigos(codigo: str, termo: str) -> Dict[str, str]:
    """Busca literal do termo no texto dos artigos."""
    artigos_encontrados = {}
    termo_lower = termo.lower()
    for artigo, texto in CODES[codigo]["Artigos"].items():
        if termo_lower in texto.lower():
            artigos_encontrados[artigo] = texto
    return artigos_encontrados


def buscar_semelhantes(codigo: str, termo: str, limite=0.5) -> Dict[str, str]:
    """Busca aproximada (semântica simples) com base em similaridade de strings."""
    artigos_semelhantes = {}
    termo_lower = termo.lower()
    for artigo, texto in CODES[codigo]["Artigos"].items():
        ratio = difflib.SequenceMatcher(None, termo_lower, texto.lower()).ratio()
        if limite <= ratio < 1.0:
            artigos_semelhantes[artigo] = texto
    return artigos_semelhantes


def gerar_citacao_abnt(codigo: str, artigo: str) -> str:
    """Gera referência ABNT automática."""
    base = CODES[codigo]["Lei"]
    return f"BRASIL. {codigo}. {base}. Diário Oficial da União, Brasília, DF. Art. {artigo}."


# =====================================================
# INTERFACE STREAMLIT
# =====================================================

st.set_page_config(page_title="LexFinder ⚖️", page_icon="⚖️", layout="wide")

st.title("⚖️ LexFinder — Buscador Inteligente de Artigos Jurídicos")
st.markdown("Pesquise por palavras-chave nos principais diplomas legais brasileiros.")

# Barra lateral (filtros)
st.sidebar.header("Filtros de busca")
codigo_escolhido = st.sidebar.selectbox("Escolher código (opcional)", ["Todos"] + list(CODES.keys()))
termo = st.sidebar.text_input("Digite uma palavra ou expressão", "")
botao = st.sidebar.button("Pesquisar")

if botao and termo:
    st.divider()
    st.subheader(f"🔍 Resultados para: **{termo}**")

    codigos_para_buscar = list(CODES.keys()) if codigo_escolhido == "Todos" else [codigo_escolhido]
    resultados_encontrados = {}
    semelhantes_encontrados = {}

    for cod in codigos_para_buscar:
        encontrados = buscar_artigos(cod, termo)
        semelhantes = buscar_semelhantes(cod, termo)
        if encontrados:
            resultados_encontrados[cod] = encontrados
        if semelhantes:
            semelhantes_encontrados[cod] = semelhantes

    if not resultados_encontrados and not semelhantes_encontrados:
        st.warning("Nenhum artigo encontrado.")
    else:
        # Resultados exatos
        for cod, artigos in resultados_encontrados.items():
            st.markdown(f"### 📘 {cod}")
            for art, texto in artigos.items():
                with st.expander(f"Art. {art}"):
                    st.write(texto)
                    citacao = gerar_citacao_abnt(cod, art)
                    st.code(citacao, language="markdown")

        # Resultados semelhantes
        if semelhantes_encontrados:
            st.markdown("---")
            st.markdown("### 💡 Você também pode se interessar por estes:")
            for cod, artigos in semelhantes_encontrados.items():
                st.markdown(f"#### 📚 {cod}")
                for art, texto in artigos.items():
                    with st.expander(f"Art. {art}"):
                        st.write(texto)
                        citacao = gerar_citacao_abnt(cod, art)
                        st.code(citacao, language="markdown")

else:
    st.info("Digite um termo e clique em **Pesquisar** para começar.")

# Rodapé
st.markdown("---")
st.markdown("👩‍💻 Desenvolvido por [Seu Grupo] — Projeto de Programação e Direito")
st.markdown("📚 Fonte: Dados simulados. Futuras versões utilizarão API pública (ex: LexML).")
