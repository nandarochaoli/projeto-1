import streamlit as st
import re
import os
import time
from google import genai
from google.genai.errors import APIError

# =========================================================================
# CONFIGURAÇÃO DE PÁGINA (ADICIONADO PARA USAR TELA TODA)
# =========================================================================

st.set_page_config(
    page_title="📍Mapa da Lei",
    layout="wide", # <-- MODO WIDE ATIVADO PARA USAR A LARGURA MÁXIMA
    initial_sidebar_state="auto"
)

# =========================================================================
# CONFIGURAÇÃO CENTRALIZADA
# =========================================================================

# Configuração de todas as leis, incluindo arquivo, sigla e âncora
LEIS_CONFIG = {
    "1. Constituição Federal": {"file": "constituicao.txt", "sigla": "CF", "anchor": "cf_anchor", "emoji": "🇧🇷"},
    "2. Código Civil": {"file": "codigo_civil.txt", "sigla": "CC", "anchor": "cc_anchor", "emoji": "🙋‍♀️"},
    "3. Código Penal": {"file": "codigo_penal.txt", "sigla": "CP", "anchor": "cp_anchor", "emoji": "🚨"},
    "4. Código de Processo Civil": {"file": "codigo_processo_civil.txt", "sigla": "CPC", "anchor": "cpc_anchor", "emoji": "👥"},    
    "5. Código de Processo Penal": {"file": "codigo_processo_penal.txt", "sigla": "CPP", "anchor": "cpp_anchor", "emoji": "👨‍⚖️"},
    "6. Código de Defesa do Consumidor": {"file": "codigo_defesa_consumidor.txt", "sigla": "CDC", "anchor": "cdc_anchor", "emoji": "🛍️"},
    "7. Código Tributário Nacional": {"file": "codigo_tributario_nacional.txt", "sigla": "CTN", "anchor": "ctn_anchor", "emoji": "💵"},
    "8. Consolidação das Leis de Trabalho": {"file": "consolidacao_leis_trabalho.txt", "sigla": "CLT", "anchor": "clt_anchor", "emoji": "👷"},
}

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
            # CHAMADA DA API
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

def buscar_em_arquivo(termo_pesquisa, nome_arquivo, sigla_lei):
    """
    Busca um termo em um arquivo de texto. A busca é exata (substring literal).
    
    Se o termo_pesquisa contiver vírgulas (,), a busca exigirá que TODAS 
    as expressões separadas por vírgula estejam presentes no artigo (lógica AND).
    """
    encontrados = []

    termo_limpo = termo_pesquisa.strip()
    
    # 1. Determina os termos OBRIGATÓRIOS (requeridos)
    if not termo_limpo:
        return []

    if ',' in termo_limpo:
        # Se houver vírgula, dividimos em termos exatos obrigatórios (lógica AND)
        # Limpa espaços e converte para minúsculas
        required_terms = [t.strip().lower() for t in termo_limpo.split(',') if t.strip()]
    else:
        # Se for um termo único, a lista de requeridos é apenas ele
        required_terms = [termo_limpo.lower()]
    
    # Se a lista de termos requeridos estiver vazia após a limpeza (ex: só vírgulas), retorna vazio.
    if not required_terms:
        return []

    try:
        with open(nome_arquivo, 'r', encoding='utf-8-sig') as f:
            conteudo_completo = f.read()
            
            # Divide o conteúdo da lei em artigos
            artigos = re.split(r'(\sArt\.\s[\d\.]+)', conteudo_completo)

            for i in range(1, len(artigos), 2):
                numero_artigo = artigos[i].strip()
                texto_do_artigo = artigos[i+1].strip()
                texto_do_artigo_lower = texto_do_artigo.lower()

                # 2. Verifica se TODAS as substrings requeridas estão presentes
                match = all(req_term in texto_do_artigo_lower for req_term in required_terms)
                
                if match:
                    
                    preview = formatar_artigo(texto_do_artigo)
                    
                    # O label inclui a sigla da lei para melhor identificação
                    encontrados.append({
                        "id": f"{nome_arquivo}_{numero_artigo}",
                        "numero": numero_artigo,
                        "preview": preview,
                        "label": f"{sigla_lei} - {numero_artigo} | {preview}", 
                        "texto_completo": f"{numero_artigo}{texto_do_artigo}"
                    })
            
    except FileNotFoundError:
        # Adiciona o campo 'label' para evitar KeyError na seção de IA.
        error_message = f"🚨 ERRO: O arquivo '{nome_arquivo}' não foi encontrado!"
        return [
            {
                "id": "error", 
                "numero": "ERRO", 
                "preview": error_message,
                "label": error_message,
                "texto_completo": ""
            }
        ]

    return encontrados


def executar_busca_completa(termo_pesquisa):
    """Executa a busca em todas as leis, armazena o total e retorna os resultados agrupados por lei."""
    resultados_por_lei = {}
    st.session_state.todos_resultados = [] # Reset lista total para o multiselect

    for titulo, config in LEIS_CONFIG.items():
        resultados = buscar_em_arquivo(termo_pesquisa, config['file'], config['sigla'])
        resultados_por_lei[titulo] = resultados
        st.session_state.todos_resultados.extend(resultados)
        
    return resultados_por_lei

def exibir_resultados_secao(titulo, resultados, anchor_name):
    """Exibe os resultados detalhados de uma única seção."""
    # Não inclui st.markdown("---") no início (única linha é após os atalhos)
    termo_pesquisa = st.session_state.termo_anterior

    # ÂNCORA HTML INSERIDA PARA NAVEGAÇÃO
    st.markdown(f'<a name="{anchor_name}"></a>', unsafe_allow_html=True)
    st.header(titulo) # Título da Seção (ex: 1. Constituição Federal)

    if resultados and resultados[0]['numero'] == "ERRO":
        # Verifica se é um erro de FileNotFoundError
        if resultados[0]['id'] == "error":
             st.error(resultados[0]['preview'])
        else:
             st.error("🚨 ERRO: Resultado inesperado durante a busca.")
        return

    num_encontrados = len(resultados)
        
    if num_encontrados > 0:
        st.success(f"✅ Termo encontrado em {num_encontrados} Artigos:")
        
        for resultado in resultados:
            st.markdown(f"**{resultado['numero']}:** {resultado['preview']}")
    else:
        st.info(f"❌ Termo '{termo_pesquisa}' não encontrado.")

# =========================================================================
# ESTRUTURA DO APLICATIVO STREAMLIT
# =========================================================================

# NOTA: O título e cabeçalho da página foram movidos para st.set_page_config
st.title("📍Mapa da Lei")
st.subheader("Encontre o caminho nas leis sem se perder.")
st.text("Base de dados conta com: CF/88, CC/02, CP/40, CPP/41, CDC/90 atualizados até o dia 10/11/2025.")

# 1. Interação do Usuário
# O placeholder foi atualizado para remover a instrução sobre aspas
termo_pesquisa = st.text_input(
    "Digite a palavra ou expressão para buscar (Se quiser buscar dois termos, use vírgula para separá-los):",
    placeholder="Ex: dignidade da pessoa humana"
)

# Inicialização do Session State
if 'todos_resultados' not in st.session_state:
    st.session_state.todos_resultados = []
if 'explicacoes_geradas' not in st.session_state:
    st.session_state.explicacoes_geradas = []
# Variável para rastrear o termo de pesquisa anterior
if 'termo_anterior' not in st.session_state:
    st.session_state.termo_anterior = ""


# 2. Execução da Lógica: A busca só ocorre se o usuário digitar algo
if termo_pesquisa:
    
    # -----------------------------------------------------------
    # FIX: Verifica se o termo mudou para decidir se limpa o multiselect.
    # -----------------------------------------------------------
    termo_mudou = (termo_pesquisa != st.session_state.termo_anterior)

    # Limpa os resultados da busca e as explicações (sempre que o termo está preenchido)
    st.session_state.todos_resultados = []
    st.session_state.explicacoes_geradas = [] 

    # SÓ LIMPA O MULTISELECT SE O TERMO DE PESQUISA MUDOU
    if termo_mudou:
        if 'selecao_artigos_ia_multiselect' in st.session_state:
            st.session_state.selecao_artigos_ia_multiselect = []

    # Atualiza o termo anterior para rastreamento
    st.session_state.termo_anterior = termo_pesquisa

    # ------------------ INÍCIO DO BLOCO INDENTADO ------------------
    
    # 1. Executa todas as buscas e armazena os resultados
    resultados_por_lei = executar_busca_completa(termo_pesquisa)
    
    # 2. Exibe os Atalhos Jurídicos (Vertical e com Contagem)
    st.markdown("### Atalhos jurídicos:")
    
    for titulo, config in LEIS_CONFIG.items():
        resultados = resultados_por_lei[titulo]
        num_encontrados = len(resultados)
        
        # Obtém o nome da lei sem a numeração (ex: Constituição Federal)
        nome_limpo = titulo.split(". ", 1)[-1].strip()
        
        # Display: [Emoji] Nome da Lei com link (vertical)
        st.markdown(f"**{config['emoji']} [{nome_limpo}](#{config['anchor']})**", unsafe_allow_html=True)
        # Display: X artigos mapeados
        
        # Exibe a contagem, tratando o caso de erro de arquivo
        if resultados and resultados[0]['numero'] == "ERRO":
             st.caption(f"**Falha ao carregar o arquivo.**")
        else:
             st.caption(f"**{num_encontrados}** artigos mapeados") 

    # Separador único solicitado, após os atalhos e antes dos resultados detalhados
    st.markdown("---")
    
    # 3. Exibe os Resultados Detalhados das Seções
    for titulo, resultados in resultados_por_lei.items():
        config = LEIS_CONFIG[titulo]
        # Esta função exibe a âncora, o título e os resultados da busca
        exibir_resultados_secao(titulo, resultados, config['anchor']) 

    # =========================================================================
    # MULTISELECT PARA SELEÇÃO E LÓGICA DE EXPLICAÇÃO POR IA
    # =========================================================================
    
    if len(st.session_state.todos_resultados) > 0:
        
        # >>> INSERÇÃO DO SEPARADOR E TÍTULO DA SEÇÃO DE IA <<<
        st.markdown("---")
        st.subheader("💡 Tradução do Jurisdiquês")
    
        # >>> FIM DA INSERÇÃO <<<

        # Lista de labels formatados para o multiselect
        labels_disponiveis = [res['label'] for res in st.session_state.todos_resultados]
        
        # Filtra quaisquer labels de erro que possam ter sido adicionados
        labels_validos = [label for label in labels_disponiveis if not label.startswith("🚨 ERRO")]


        # 1. Componente Multiselect para seleção dos artigos (Máximo 3)
        selecao_labels = st.multiselect(
            "Selecione **até 3** artigos:",
            options=labels_validos,
            key='selecao_artigos_ia_multiselect'
        )
        
        selecionados_final = selecao_labels[:3]
        
        if len(selecao_labels) > 3:
            st.warning("⛔ Você selecionou mais de 3 artigos. Apenas os 3 primeiros serão processados.")

        st.info(f"Artigos prontos para explicação: **{len(selecionados_final)} / 3**")
        
        # 2. Botão para acionar a IA
        if st.button("Explicar artigos", key="explicar_button"):
            
            if not selecionados_final:
                st.warning("⚠️ Selecione pelo menos um artigo para que eu possa explicar.")
            else:
                # 3. Mapeia os labels selecionados de volta para os objetos de artigo
                mapa_resultados = {res['label']: res for res in st.session_state.todos_resultados}
                artigos_selecionados = [mapa_resultados[label] for label in selecionados_final]

                # 4. Configura e Chama a API
                client = configurar_api()
                
                if client:
                    
                    with st.spinner(f"Processando {len(artigos_selecionados)} artigo(s)... A inteligência artificial está trabalhando para simplificar o texto legal."):
                        
                        # Limpa o estado e gera a nova lista de explicações
                        st.session_state.explicacoes_geradas = []
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
        st.markdown("🔎 Decifrando Artigos")
        
        for item in st.session_state.explicacoes_geradas:
            st.markdown(f"### {item['numero']}")
            
            # Exibe o artigo completo
            st.code(item['texto_completo'], language='markdown')
            
            # Exibe a explicação da IA
            st.markdown("**✍️ Explicação cuidadosa do texto legal:**")
            st.markdown(item['explicacao'])
            st.markdown("---")
            
    st.markdown("---")
