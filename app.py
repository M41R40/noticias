import streamlit as st
import json
import os

st.set_page_config(page_title="Timeline de Notícias Políticas", page_icon="📰", layout="wide")

ARQUIVO_HISTORICO = "historico_noticias.json"

def carregar_noticias():
    if os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

st.title("📰 Painel de Notícias Políticas - Brasil")
st.caption("Atualizado automaticamente via GitHub Actions com base em Dorks.")

if st.button("🔄 Recarregar Tela"):
    st.rerun()

noticias = carregar_noticias()

if noticias:
    st.markdown("---")
    dorks_disponiveis = list(set([item["dork"] for item in noticias]))
    dork_selecionada = st.selectbox("🔍 Filtrar por Dork:", ["Todas as Dorks"] + dorks_disponiveis)

    if dork_selecionada != "Todas as Dorks":
        noticias_filtradas = [item for item in noticias if item["dork"] == dork_selecionada]
    else:
        noticias_filtradas = noticias

    st.write(f"Exibindo **{len(noticias_filtradas)}** notícias.")

    for item in noticias_filtradas:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.caption(f"🕒 Capturado em:\n{item['capturado_em']}")
            st.caption(f"🗓️ Publicado:\n{item['data_publicacao']}")
        with col2:
            st.markdown(f"📌 **Dork:** `{item['dork']}`")
            st.markdown(f"### [{item['titulo']}]({item['link']})")
            st.caption(f"📰 Fonte: {item['fonte']}")
        st.divider()
else:
    st.warning("Nenhuma notícia encontrada. Aguarde a primeira execução do robô no GitHub ou envie um `historico_noticias.json` inicial.")