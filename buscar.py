# Importa uma biblioteca para lidar melhor com a formatação dos artigos
import re

def formatar_artigo(texto_artigo):
    """Pega os primeiros 150 caracteres do artigo para dar um 'preview'."""
    # Remove espaços em branco extras e quebras de linha do início
    preview = texto_artigo.strip()
    
    # Pega os primeiros 150 caracteres
    if len(preview) > 150:
        preview = preview[:150] + "..."
    
    return preview

def buscar_em_arquivo(termo_pesquisa, nome_arquivo):
    """
    Função principal que busca um termo em um arquivo de texto.
    Ela divide o texto por 'Art.' e procura o termo em cada artigo.
    """
    print(f"\n--- 🔎 Buscando em: {nome_arquivo} ---")
    encontrados = []

    try:
        # 'utf-8-sig' ajuda a ignorar caracteres 'estranhos' que podem vir da web
        with open(nome_arquivo, 'r', encoding='utf-8-sig') as f:
            # Lê o conteúdo completo do arquivo
            conteudo_completo = f.read()
            
            # Divide o texto todo vez que encontrar "Art."
            # (Usamos 're.split' para manter o número do artigo)
            # A expressão '(\sArt\.\s\d+)' significa:
            # \s = espaço, Art\. = "Art.", \s = espaço, \d+ = um ou mais números
            artigos = re.split(r'(\sArt\.\s\d+)', conteudo_completo)

            # Iteramos de 2 em 2, pois a lista fica [texto, Art. 1, texto, Art. 2, ...]
            for i in range(1, len(artigos), 2):
                numero_artigo = artigos[i].strip() # Ex: "Art. 1"
                texto_do_artigo = artigos[i+1] # O texto que vem depois

                # Verificamos se o termo está no texto (ignorando maiúsculas/minúsculas)
                if termo_pesquisa.lower() in texto_do_artigo.lower():
                    # Se encontramos, guardamos o número e um preview
                    preview = formatar_artigo(texto_do_artigo)
                    encontrados.append(f"  ➡️  {numero_artigo}º: \"{preview}\"")

        # Depois de verificar todos os artigos, mostramos os resultados
        if encontrados:
            print(f"✅ Termo '{termo_pesquisa}' encontrado em {len(encontrados)} artigos:")
            for item in encontrados:
                print(item)
        else:
            print(f"❌ Termo '{termo_pesquisa}' não encontrado em {nome_arquivo}.")
            
    except FileNotFoundError:
        print(f"🚨 ERRO: O arquivo '{nome_arquivo}' não foi encontrado!")
        print("Por favor, verifique se ele está na mesma pasta do script.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

# --- Início do Programa ---
print("====================================")
print("  Buscador de Leis - CF e Código Civil")
print("====================================")

# Pede ao usuário o termo para buscar
termo = input("Digite a palavra ou expressão exata que deseja buscar: ")

if termo:
    # Chama a função de busca para cada arquivo
    buscar_em_arquivo(termo, "constituicao.txt")
    buscar_em_arquivo(termo, "codigo_civil.txt")
else:
    print("Nenhum termo digitado. Encerrando.")

print("\n--- Fim da busca ---")
