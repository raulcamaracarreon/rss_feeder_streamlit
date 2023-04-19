import streamlit as st
import feedparser
from bs4 import BeautifulSoup

# Añadir las URL de feeds por defecto
default_feeds = [
    'http://imparcialoaxaca.mx/feed/',
    'https://www.elsiglodetorreon.com.mx/index.xml',
    'https://www.mural.com.mx/rss/portada.xml',
    'https://diario.mx/jrz/media/sitemaps/rss.xml',
    'https://www.sinembargo.mx/feed',
    'https://www.elnorte.com/rss/portada.xml',
    'http://expresochiapas.com/noticias/feed/'
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

st.title('RSS Feed Reader')

url = st.text_input('Enter the RSS feed URL’', value=",".join(default_feeds))
keyword = st.text_input('Filter by keyword (optional)')

max_articles = st.slider('Maximum number of articles to show', min_value=1, max_value=100, value=10)

urls = url.split(",")

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
            
            st.write(article.summary)
            
            # Mostrar la fecha de publicación o actualización
            if hasattr(article, 'published'):
                st.write('**Published:**', article.published)
            elif hasattr(article, 'updated'):
                st.write('**Updated:**', article.updated)


