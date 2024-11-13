import streamlit as st
import openai
import pandas as pd
import search_utils
from pinecone import Pinecone


search_utils.set_page_configuration(initial_sidebar_state="collapsed")

# OpenAI setup using Streamlit secrets
openai.api_key = st.secrets["openai"]["api_key"]

# Pinecone API key setup using Streamlit secrets
pinecone_api_key = st.secrets["pinecone"]["api_key"]

# Pinecone setup
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index("mollat-serverless")

# title = "Trouvez le livre qui vous convient"

# st.image("https://www.mollat.com/Content/Img/Layout/logo.png")
st.markdown(
    """
    <div style='text-align: center;'>
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Logotype_Mollat_RVB.pdf/page1-1200px-Logotype_Mollat_RVB.pdf.jpg" alt="Mollat Logo" width="300">
    </div>
    """,
    unsafe_allow_html=True,
)

# st.markdown(
#     f"<h1 style='text-align: center;font-size:50px;'>{title}</h1>",
#     unsafe_allow_html=True,
# )

st.write("")
st.write("")

# st.write("Type any niche")

search_input = st.text_input(
    "Qu'avez-vous envie de lire aujourd'hui ?",
    # "",
)


if len(search_input) > 0:
    embedding = search_utils.get_embedding(search_input, model="text-embedding-ada-002")
    results = index.query(
        vector=embedding,
        top_k=30,
        include_values=True,
        namespace="mollat-serverless",
        # filter=filter,
        includeMetadata=True,
    )

    (
        # id,
        title,
        authors,
        link,
        published_date,
        publisher,
        book_picture_url,
        coup_de_coeur,
        summary,
        score,
    ) = ([], [], [], [], [], [], [], [], [])

    for el in results["matches"]:
        # account_name.append(el["metadata"]["account_name"])
        # id.append(el["id"])
        title.append(el["metadata"]["title"])
        link.append(el["metadata"]["link"])
        authors.append(el["metadata"]["authors"])
        published_date.append(el["metadata"]["published_date"])
        publisher.append(el["metadata"]["publisher"])
        book_picture_url.append(el["metadata"]["book_picture_url"])
        coup_de_coeur.append(el["metadata"]["coup_de_coeur"])
        summary.append(el["metadata"]["summary"])
        score.append(str(round(el["score"] * 100, 2)) + "%")

    st.write("")
    st.markdown(
        f"<h5>Voici ce que nous avons trouvé pour vous !</h5>",
        unsafe_allow_html=True,
    )
    st.write("")
    for i in range(30):
        st.write("")
        search_utils.display_book(
            pd.DataFrame(
                {
                    # "id": id[i],
                    "authors": authors[i],
                    "title": title[i],
                    "link": link[i],
                    "published_date": published_date[i],
                    "publisher": publisher[i],
                    "book_picture_url": book_picture_url[i],
                    "coup_de_coeur": coup_de_coeur[i],
                    "summary": summary[i],
                    "score": score[i],
                },
                index=[0],
            ),
            search_input,
        )

for _ in range(4):
    st.write("")
