import streamlit as st
import re
import os
import time
from google import genai
from google.genai.errors import APIError

# =========================================================================
# CONFIGURAÇÃO E FUNÇÕES DA API (IA)
# =========================================================================

def configurar_api():
    """
    Configura a chave da API Gemini.
    A chave deve ser definida como um 'Secret' no Streamlit Cloud.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.error(
            "🚨 ERRO DE CONFIGURAÇÃO: A chave 'GEMINI_API_KEY' não foi encontrada. "
            "Por favor, configure-a nos Streamlit Secrets para usar a função de IA."
        )
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Erro ao inicializar o cliente Gemini: {e}")
        return None


def gerar_explicacao_ia(client, artigo_completo):
    """
    Chama a API Gemini para gerar uma explicação simplificada do artigo.
    O 'system_prompt' foi incorporado ao 'user_prompt' para contornar o erro de SDK.
    """
    # System Instruction incorporada ao prompt para garantir a compatibilidade com o SDK
    system_instruction = (
        "INSTRUÇÃO DE ROLEPLAY: Você é um tutor jurídico prestativo. Sua tarefa é simplificar textos legais "
        "complexos (artigos de lei) para que sejam compreendidos por leigos. "
        "Sua resposta deve ser escrita em linguagem clara, acessível e objetiva, "
        "evitando jargões desnecessários, mantendo a fidelidade ao sentido legal."
    )

    user_prompt = (
        f"{system_instruction}\n\n"
        "Com base no seu roleplay, por favor, analise o seguinte artigo de lei e forneça uma explicação "
        "com linguagem simples e acessível. Mantenha o tom de um tutor amigo. "
        f"Artigo: \n\n{artigo_completo}"
    )
    
    # Exponential Backoff para lidar com rate limits
    MAX_RETRIES = 5
    delay = 1  # Atraso inicial em segundos

    for attempt in range(MAX_RETRIES):
        try:
            # CHAMADA DA API CORRIGIDA: Removido o argumento 'system_instruction'
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_prompt
            )
            return response.text
        except APIError as e:
            if attempt < MAX_RETRIES - 1:
                st.warning(f"Erro na API (Tentativa {attempt + 1}/{MAX_RETRIES}). Tentando novamente em {delay}s...")
                time.sleep(delay)
                delay *= 2  # Aumenta o atraso
            else:
                st.error(f"Falha ao gerar explicação após {MAX_RETRIES} tentativas. Erro final: {e}")
                return "Não foi possível gerar a explicação. Tente novamente mais tarde."
        except Exception as e:
            # Captura o erro anterior e o loga para depuração
            st.error(f"Erro inesperado durante a chamada da API: {e}")
            return "Erro desconhecido ao processar a requisição."
    return "Falha total na comunicação com a API."

# =========================================================================
# FUNÇÕES DE BUSCA (Lógica)
# =========================================================================

def formatar_artigo(texto_artigo):
    """Pega os primeiros 300 caracteres do artigo para dar um 'preview'."""
    LIMITE_PREVIEW = 300
    preview = texto_artigo.strip()

    if len(preview) > LIMITE_PREVIEW:
        preview = preview[:LIMITE_PREVIEW] + "..."

    # Remove quebras de linha e múltiplos espaços do preview para exibição limpa
    preview = re.sub(r'\s+', ' ', preview)
    
    return preview

def buscar_em_arquivo(termo_pesquisa, nome_arquivo):
    """
    Busca um termo em um arquivo de texto e retorna uma lista de dicionários.
    Cada dicionário contém o ID, preview e texto completo do artigo.
    """
    encontrados = []

    if not termo_pesquisa:
        return []

    try:
        with open(nome_arquivo, 'r', encoding='utf-8-sig') as f:
            conteudo_completo = f.read()
            
            # Permite a captura de números de artigo com pontos (ex: Art. 1.762)
            artigos = re.split(r'(\sArt\.\s[\d\.]+)', conteudo_completo)

            for i in range(1, len(artigos), 2):
                numero_artigo = artigos[i].strip()
                texto_do_artigo = artigos[i+1].strip()
                
                # A busca é feita de forma case-insensitive
                if termo_pesquisa.lower() in texto_do_artigo.lower():
                    preview = formatar_artigo(texto_do_artigo)
                    
                    encontrados.append({
                        "id": f"{nome_arquivo}_{numero_artigo}",
                        "numero": numero_artigo,
                        "preview": preview,
                        "texto_completo": f"{numero_artigo}{texto_do_artigo}"
                    })
            
    except FileNotFoundError:
        # Retorna erro no formato esperado para ser tratado na UI
        return [
            {"id": "error", "numero": "ERRO", "preview": f"🚨 ERRO: O arquivo '{nome_arquivo}' não foi encontrado!", "texto_completo": ""}
        ]

    return encontrados

def get_selected_count():
    """
    Retorna a contagem de artigos selecionados na página.
    Procura por chaves que contenham '.txt', pois são os identificadores dos artigos.
    """
    count = 0
    # Verifica o estado de todos os checkboxes no session_state
    for key, value in st.session_state.items():
        if isinstance(key, str) and '.txt' in key and value is True:
            count += 1
    return count

def exibir_secao(titulo, nome_arquivo, termo_pesquisa, anchor_name, key_prefix):
    """Exibe uma seção de busca (CF, CC, etc.) com seus resultados."""
    st.markdown("---")
    # ÂNCORA HTML INSERIDA PARA NAVEGAÇÃO
    st.markdown(f'<a name="{anchor_name}"></a>', unsafe_allow_html=True)
    st.header(titulo)

    resultados = buscar_em_arquivo(termo_pesquisa, nome_arquivo)
    
    # Tratamento de erro de arquivo
    if resultados and resultados[0]['numero'] == "ERRO":
        st.error(resultados[0]['preview'])
        return
        
    st.session_state.todos_resultados.extend(resultados)
    
    if len(resultados) > 0:
        st.success(f"✅ Termo encontrado em {len(resultados)} Artigos de {titulo.split('. ')[1]}:")
        
        for i, resultado in enumerate(resultados):
            
            # 1. Lógica de Limite de Seleção
            limite_excedido = get_selected_count() >= 3
            # A chave completa agora é usada para verificar o estado
            chave_completa = f"{key_prefix}_{resultado['id']}" 
            esta_marcado = st.session_state.get(chave_completa, False)
            
            # O checkbox é desabilitado se o limite for atingido E o artigo não estiver marcado
            disabled = limite_excedido and not esta_marcado

            col_check, col_artigo = st.columns([0.05, 0.95])
            
            # Adiciona o checkbox com a regra de 'disabled'
            with col_check:
                st.checkbox(
                    "", 
                    # Chave única garantida
                    key=chave_completa, 
                    value=esta_marcado, # Usa o estado real para manter a marcação
                    label_visibility="collapsed",
                    disabled=disabled
                )
            
            with col_artigo:
                # Exibe o preview do artigo
                st.markdown(f"**{resultado['numero']}:** {resultado['preview']}")
    else:
        st.info(f"❌ Termo '{termo_pesquisa}' não encontrado em {titulo.split('. ')[1]}.")


# =========================================================================
# ESTRUTURA DO APLICATIVO STREAMLIT
# =========================================================================

# Título e cabeçalho da página
st.title("🏛️ Buscador Jurídico Rápido")
st.subheader("A ferramenta tem como base: CF/88, CC/02, CP/40, CPP/41, CDC/90 atualizados até o dia 05/11/2025.")

# 1. Interação do Usuário
termo_pesquisa = st.text_input(
    "Digite a palavra ou expressão exata que deseja buscar:",
    placeholder="Ex: dignidade da pessoa humana"
)

# Inicialização do Session State
if 'todos_resultados' not in st.session_state:
    st.session_state.todos_resultados = []
if 'explicacoes_geradas' not in st.session_state:
    st.session_state.explicacoes_geradas = []

# 2. Execução da Lógica: A busca só ocorre se o usuário digitar algo
if termo_pesquisa:
    # -----------------------------------------------------------
    # FIX CRÍTICO: Limpa todas as chaves de checkbox antigas
    # Garante que o Streamlit não confunda componentes de renderizações passadas.
    keys_to_delete = [k for k in st.session_state if isinstance(k, str) and ('.txt' in k or k.startswith('cf_') or k.startswith('cc_'))]
    for k in keys_to_delete:
        try:
            del st.session_state[k]
        except KeyError:
            pass # Ignora se a chave já foi deletada
    # -----------------------------------------------------------

    # Limpa a lista de resultados (mantendo as explicações geradas até o novo clique)
    st.session_state.todos_resultados = []

    # ------------------ INÍCIO DO BLOCO INDENTADO ------------------
    
    # 2. BOTÕES DE NAVEGAÇÃO RÁPIDA (Aparecem com o termo de pesquisa)
    st.markdown("---")
    st.markdown("### Navegação Rápida (Clique para rolar até a seção)")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Usando st.markdown com links de âncora
    with col1: st.markdown("[🇧🇷 CF](#cf_anchor)", unsafe_allow_html=True)
    with col2: st.markdown("[🤵 CC](#cc_anchor)", unsafe_allow_html=True)
    with col3: st.markdown("[🚨 CP](#cp_anchor)", unsafe_allow_html=True)
    with col4: st.markdown("[⚖️ CPP](#cpp_anchor)", unsafe_allow_html=True)
    with col5: st.markdown("[🛍️ CDC](#cdc_anchor)", unsafe_allow_html=True)

    st.markdown("---")
    
    # --- Execução das Buscas ---
    
    exibir_secao("1. Constituição Federal", "constituicao.txt", termo_pesquisa, "cf_anchor", "cf")
    exibir_secao("2. Código Civil", "codigo_civil.txt", termo_pesquisa, "cc_anchor", "cc")
    exibir_secao("3. Código Penal", "codigo_penal.txt", termo_pesquisa, "cp_anchor", "cp")
    exibir_secao("4. Código de Defesa do Consumidor", "codigo_defesa_consumidor.txt", termo_pesquisa, "cdc_anchor", "cdc")
    exibir_secao("5. Código de Processo Penal", "codigo_processo_penal.txt", termo_pesquisa, "cpp_anchor", "cpp")

    # =========================================================================
    # BOTÃO E LÓGICA DE EXPLICAÇÃO POR IA
    # =========================================================================
    
    st.markdown("---")
    
    # Exibe a contagem e aviso de limite
    if len(st.session_state.todos_resultados) > 0:
        selecionados = get_selected_count()
        if selecionados >= 3:
            st.warning("⛔ Limite de artigos selecionados (máximo de 3) atingido.")
        st.info(f"Artigos selecionados para explicação: **{selecionados} / 3**")
        
        # O botão que aciona a explicação
        if st.button("🤖 Explique os artigos selecionados para mim", key="explicar_button"):
            artigos_selecionados = []
            
            # 1. Coleta os artigos marcados
            for resultado in st.session_state.todos_resultados:
                
                # Obtemos o prefixo da seção a partir do nome do arquivo (necessário para reconstruir a chave)
                if resultado['id'].startswith("constituicao.txt"):
                    prefixo = 'cf'
                elif resultado['id'].startswith("codigo_civil.txt"):
                    prefixo = 'cc'
                elif resultado['id'].startswith("codigo_penal.txt"):
                    prefixo = 'cp'
                elif resultado['id'].startswith("codigo_defesa_consumidor.txt"):
                    prefixo = 'cdc'
                elif resultado['id'].startswith("codigo_processo_penal.txt"):
                    prefixo = 'cpp'
                else:
                    continue # Pula resultados inválidos
                
                chave_completa = f"{prefixo}_{resultado['id']}"
                
                # Verifica se o checkbox para esta chave foi marcado
                if st.session_state.get(chave_completa, False):
                    artigos_selecionados.append(resultado)
            
            if not artigos_selecionados:
                st.warning("⚠️ Selecione pelo menos um artigo para que eu possa explicar.")
            else:
                # 2. Configura a API
                client = configurar_api()
                
                if client:
                    st.session_state.explicacoes_geradas = []
                    # 3. Gera as explicações com um spinner de carregamento
                    with st.spinner(f"Processando {len(artigos_selecionados)} artigo(s)... A inteligência artificial está trabalhando para simplificar o texto legal."):
                        
                        for artigo in artigos_selecionados:
                            explicacao = gerar_explicacao_ia(client, artigo['texto_completo'])
                            
                            st.session_state.explicacoes_geradas.append({
                                "numero": artigo['numero'],
                                "texto_completo": artigo['texto_completo'],
                                "explicacao": explicacao
                            })
                    
                    st.success("✅ Explicações geradas com sucesso! Role para baixo.")
    
    # =========================================================================
    # EXIBIÇÃO DAS EXPLICAÇÕES GERADAS
    # =========================================================================
    
    if st.session_state.explicacoes_geradas:
        st.markdown('<a name="explicacoes_anchor"></a>', unsafe_allow_html=True)
        st.markdown("## 🧠 Explicações Jurídicas Simplificadas")
        
        for item in st.session_state.explicacoes_geradas:
            st.markdown(f"### {item['numero']}")
            
            # Exibe o artigo completo
            st.code(item['texto_completo'], language='markdown')
            
            # Exibe a explicação da IA
            st.markdown("**✍️ Explicação Acessível (Tutor IA):**")
            st.markdown(item['explicacao'])
            st.markdown("---")
            
    st.markdown("---")
    # ------------------ FIM DO BLOCO INDENTADO ------------------
