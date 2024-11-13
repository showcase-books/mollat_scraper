import streamlit as st
import openai
import re
import json
import requests
from PIL import Image
from io import BytesIO


def set_page_configuration(initial_sidebar_state="expanded"):
    return st.set_page_config(
        page_title="Mollat - Moteur de recherche",
        page_icon="📚",
        # layout="wide",
        initial_sidebar_state=initial_sidebar_state,
        menu_items={
            # 'Get Help': 'https://github.com/ceptln',
            # 'Report a bug': "https://github.com/ceptln",
            # 'About': "This app was built an deployed by Camille Goat Epitalon"
        },
    )


def open_file(filepath):
    with open(filepath, "r", encoding="utf-8") as infile:
        return infile.read()


def get_embedding(text: str, model="text-embedding-ada-002") -> list[float]:
    return openai.Embedding.create(input=[text], model=model)["data"][0]["embedding"]


import ast


def display_book(random_book, search_input):
    cols = st.columns(2)

    # Fetch the image using requests
    image_url = str(random_book["book_picture_url"].values[0])

    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            cols[0].image(img, width=200)
        else:
            st.error("Failed to load image")
    except:
        cols[0].image(str(random_book["book_picture_url"].values[0]), width=200)

    # Display book details
    cols[1].markdown(
        f"<p><u>Titre</u> : {str(random_book['title'].values[0]).title()}</p>",
        unsafe_allow_html=True,
    )
    page_link = str(random_book["link"].values[0])
    cols[1].markdown(f"[Lien de la page]({page_link})")
    cols[1].markdown(
        f"<p><u>Auteur(s)</u> : {str(random_book['authors'].values[0]).title()}</p>",
        unsafe_allow_html=True,
    )
    cols[1].markdown(
        f"<p><u>Date de publication</u> : {str(random_book['published_date'].values[0])}</p>",
        unsafe_allow_html=True,
    )
    cols[1].markdown(
        f"<p><u>Score</u> : {str(random_book['score'].values[0])} </p>",
        unsafe_allow_html=True,
    )

    # Ensure coup_de_coeur is a dictionary
    coup_de_coeur = random_book["coup_de_coeur"].values[0]
    if coup_de_coeur and isinstance(coup_de_coeur, str):
        coup_de_coeur = ast.literal_eval(coup_de_coeur)  # Convert string to dictionary

    # Only proceed if coup_de_coeur is valid and contains the required keys
    if coup_de_coeur:
        themes = coup_de_coeur.get("Themes", "").split(", ")
        title = coup_de_coeur.get("Title", "")
        content = coup_de_coeur.get("Content", "")

        # Display themes as boxes
        theme_boxes = "".join(
            [
                f"<span style='display: inline-block; border: 1px solid #ddd; padding: 4px 8px; margin: 2px; border-radius: 4px;'>{theme}</span>"
                for theme in themes
            ]
        )

        st.markdown(
            f"""
            <div style="border: 1px solid #ddd; padding: 10px; border-radius: 6px; background-color: #f9f9f9;">
                <p style="font-size: 18px; font-weight: bold;">{title}</p>
                {theme_boxes}
                <p style="margin-top: 10px;">{content}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<p><strong>Coup de Coeur:</strong> Information non disponible.</p>",
            unsafe_allow_html=True,
        )

    # Add expandable section for additional content
    summary = str(random_book["summary"].values[0])
    with st.expander("Résumé"):
        st.markdown(summary, unsafe_allow_html=True)


# def display_book(random_book, search_input):
#     cols = st.columns(2)

#     # Fetch the image using requests
#     image_url = str(random_book["book_picture_url"].values[0])

#     try:
#         response = requests.get(image_url)
#         if response.status_code == 200:
#             img = Image.open(BytesIO(response.content))
#             cols[0].image(img, width=200)
#         else:
#             st.error("Failed to load image")
#     except:
#         cols[0].image(str(random_book["book_picture_url"].values[0]), width=200)

#     # cols[0].image(str(random_book["profile_pic_url"].values[0]), width=200)
#     cols[1].markdown(
#         f"<p><u>Titre</u> : {str(random_book['title'].values[0]).title()}</p>",
#         unsafe_allow_html=True,
#     )

#     # Display profile link
#     page_link = str(random_book["link"].values[0])
#     cols[1].markdown(f"[Lien de la page]({page_link})")

#     cols[1].markdown(
#         f"<p><u>Auteur(s)</u> : {str(random_book['authors'].values[0]).title()}</p>",
#         unsafe_allow_html=True,
#     )
#     cols[1].markdown(
#         f"<p><u>Date de publication</u> : {str(random_book['published_date'].values[0])}</p>",
#         unsafe_allow_html=True,
#     )
#     # cols[1].markdown(
#     #     f"<p><u>Business categories</u> : {str(random_book['business_category_name'].values).title()} >  </p>",
#     #     unsafe_allow_html=True,
#     # )
#     cols[1].markdown(
#         f"<p><u>Score</u> : {str(random_book['score'].values[0])} </p>",
#         unsafe_allow_html=True,
#     )

#     # Function to highlight search term
#     def highlight_text(text, search_input):
#         if search_input:
#             search_pattern = re.compile(re.escape(search_input), re.IGNORECASE)
#             highlighted_text = search_pattern.sub(
#                 f"<mark style='background-color: yellow;'>{search_input}</mark>", text
#             )
#         else:
#             highlighted_text = text
#         return highlighted_text

#     # Display biography with highlight
#     coup_de_coeur = str(random_book["coup_de_coeur"].values[0])
#     # highlighted_biography = highlight_text(coup_de_coeur, search_input)
#     st.markdown(
#         # f"<p><u>Biography</u> : {highlighted_biography}</p>",
#         f"<p><u>Coup de coeur </u> : {coup_de_coeur}</p>",
#         unsafe_allow_html=True,
#     )

#     # Add expandable section for additional content with highlight
#     summary = str(random_book["summary"].values[0])
#     # highlighted_additional_content = highlight_text(summary, search_input)

#     with st.expander("Résumé"):
#         # Render highlighted additional content
#         # st.markdown(highlighted_additional_content, unsafe_allow_html=True)
#         st.markdown(summary, unsafe_allow_html=True)


# def add_filters(query: str) -> list:
#     filter = None
#     pattern = r"{(.*?)}"
#     matches = re.findall(pattern, query)
#     if matches:
#         key_value_pairs = matches[0].split(",")
#         filter = {}
#         for pair in key_value_pairs:
#             key, value = pair.split(":")
#             filter[key.strip()] = value.strip()
#         search_input = query.replace("{" + matches[0] + "}", "").lstrip()
#     else:
#         search_input = query.lstrip()

#     return filter, search_input


# def add_filters_simple(query: str) -> list:
#     filter = None
#     pattern = r"{(.*?)}"
#     matches = re.findall(pattern, query)
#     if matches:
#         filter_extract = ""
#         for char in query:
#             if char == "}":
#                 filter_extract += char
#                 break
#             filter_extract += char
#         search_input = query[len(filter_extract) + 1 :].lstrip()
#     else:
#         search_input = query.lstrip()

#     return filter_extract, search_input
