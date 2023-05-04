import streamlit as st
import feedparser
from bs4 import BeautifulSoup

# Añadir las URL de feeds por defecto
default_feeds = [
    'https://www.sinembargo.mx/feed',
    'https://www.mural.com.mx/rss/portada.xml',
    'https://diario.mx/jrz/media/sitemaps/rss.xml',
    'http://imparcialoaxaca.mx/feed/',
    'https://www.elsiglodetorreon.com.mx/index.xml',
    'https://www.elnorte.com/rss/portada.xml',
    'http://expresochiapas.com/noticias/feed/',
    'https://mexiconewsdaily.com/feed/',
]

def get_feed(url):
    feed = feedparser.parse(url)
    return feed.entries

def get_image(article):
    soup = BeautifulSoup(article.summary, 'html.parser')
    img_tag = soup.find('img')
    if img_tag:
        return img_tag['src']
    return None

def filter_articles(articles, keyword):
    return [article for article in articles if keyword.lower() in article.title.lower() or keyword.lower() in article.summary.lower()]

def clean_html(content):
    soup = BeautifulSoup(content, 'html.parser')
    return soup.get_text()

st.title('RSS Feed Reader')

url = st.text_input('Enter the RSS feed URL (You can add more than one URL by separating them with commas)', value=",".join(default_feeds))
keyword = st.text_input('Filter by keyword (optional)')

max_articles = st.slider('Maximum number of articles to show', min_value=1, max_value=100, value=25)

urls = url.split(",")

st.markdown("""
    <style>
        .stText {
            text-align: justify;
        }
    </style>
""", unsafe_allow_html=True)

for single_url in urls:
    if single_url:
        articles = get_feed(single_url)
        
        if keyword:
            articles = filter_articles(articles, keyword)

        for article in articles[:max_articles]:
            # Mostrar el título como enlace al artículo
            st.write('##', f"[{article.title}]({article.link})")
            
            # Mostrar la imagen, si la hay
            image_url = get_image(article)
            if image_url:
                st.image(image_url)
            
            # Limpiar y mostrar el resumen
            cleaned_summary = clean_html(article.summary)
            st.markdown(f'<div class="stText">{cleaned_summary}</div>', unsafe_allow_html=True)
            
            # Mostrar la fecha de publicación o actualización
            if hasattr(article, 'published'):
                st.write('**Published:**', article.published)
            elif hasattr(article, 'updated'):
                st.write('**Updated:**', article.updated)


