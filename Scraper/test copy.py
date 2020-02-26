import requests
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from bs4 import BeautifulSoup

bibtex_id = '10.1038/s41427-019-0143-9'

url = "http://www.doi2bib.org/{id}".format(id=bibtex_id)
xhr_url = 'http://www.doi2bib.org/'

with requests.Session() as session:
    session.get(url)

    response = session.get(xhr_url, params={'id': bibtex_id})
    print(response.content)