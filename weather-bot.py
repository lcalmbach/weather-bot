import streamlit as st
from langchain.adapters.openai import convert_openai_messages
from langchain_community.chat_models import ChatOpenAI
from tavily import TavilyClient

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
image_path = "./weather-bot.jpeg"

client = TavilyClient(api_key=TAVILY_API_KEY)
cols = st.columns([1, 8, 1])
with cols[1]:
    st.image(image_path, caption='Friendly Weather Expert Robot',width=600)

st.markdown("**Hallo Wetterexperte, wie war denn das Wetter in der Schweiz im**")
season = st.selectbox("", ["Winter", "Spring", "Summer", "Fall"], label_visibility="collapsed")
year = st.number_input("im Jahr", value=2020, label_visibility="collapsed")
query = f"Welche signifikanten Wetter Ereignisse gab es im {season} {year} in der Schweiz? Wie ist diese Jahreszeit mit historischen Daten vergleichbar?"
if st.button("Zusammenfassung"):
    content = client.search(query, search_depth="advanced")["results"]
    prompt = [{
        "role": "system",
        "content":  f'Du bist ein Wetter Experte und fasst das Wetter einer Jahreszeit zusammen in einem kurzen Artikel'\
                    f'Bei allen Zitaten in deinem Text erwähnst du die Quelle als verlinkte URL.'\
                    f'Halte die Zusamenfassung kurz und prägnant.'
    }, {
        "role": "user",
        "content": f'Information: """{content}"""\n\n' \
                f'Using the above information, answer the following'\
                f'query: "{query}" in a summary report --'\
                f'Please use MLA format and markdown syntax.'
    }]
    lc_messages = convert_openai_messages(prompt)
    report = ChatOpenAI(model='gpt-4o',openai_api_key=OPENAI_API_KEY).invoke(lc_messages).content
    st.markdown(report)

with st.expander("Infos zur Appp"):
    st.markdown ('Diese App wurde mit [Tavily](https://tavily.com), [OpenAI](https://openai.com), und [langchain_community](https://www.langchain.com/langchain) entwickelt. Das git-repo findest du [hier]()')