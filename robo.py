import urllib.parse
import feedparser
import json
import os
from datetime import datetime

ARQUIVO_DORKS = "dorks.txt"
ARQUIVO_HISTORICO = "historico_noticias.json"

def executar_varredura():
    print("Iniciando varredura automatizada...")
    
    if not os.path.exists(ARQUIVO_DORKS):
        print(f"ERRO: Arquivo '{ARQUIVO_DORKS}' não encontrado!")
        return

    with open(ARQUIVO_DORKS, "r", encoding="utf-8") as f:
        dorks = [linha.strip() for linha in f if linha.strip()]

    todas_noticias = []

    for dork in dorks:
        dork_codificada = urllib.parse.quote(dork)
        rss_url = f"https://news.google.com/rss/search?q={dork_codificada}&hl=pt-BR&gl=BR&ceid=BR:pt"
        
        feed = feedparser.parse(rss_url)
        
        for entry in feed.entries[:5]:  # Pega as 5 mais recentes por dork
            todas_noticias.append({
                "dork": dork,
                "titulo": entry.title,
                "link": entry.link,
                "data_publicacao": getattr(entry, "published", "Data não informada"),
                "fonte": entry.get("source", {}).get("title", "Google News"),
                "capturado_em": datetime.now().strftime("%d/%m/%Y %H:%M")
            })

    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
        json.dump(todas_noticias, f, ensure_ascii=False, indent=4)

    print(f"Varredura concluída! {len(todas_noticias)} notícias salvas.")

if __name__ == "__main__":
    executar_varredura()