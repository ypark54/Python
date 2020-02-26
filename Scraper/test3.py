import bs4 as bs
import sys
import urllib.request
from PySide2.QtWebEngineWidgets import QWebEnginePage
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QUrl, QByteArray
from PySide2.QtWebEngineCore import QWebEngineUrlRequestInterceptor, QWebEngineHttpRequest

class Page(QWebEnginePage):
    def __init__(self, url, qapp):
        self.app = qapp
        print(self.app)
        QWebEnginePage.__init__(self)
        
        self.html = ''
        #self.loadFinished.connect(self._on_load_finished)
        
        self.q = QUrl(url)
        self.req = QWebEngineHttpRequest(self.q)
        self.req.setHeader(QByteArray(1, 'a'), QByteArray(2, 'b'))
        
        print(self.req.headers())
        self.load(self.req)
        print(self.req)
        self.setHtml(self.html, self.q)
        print(self.html)
        #self.app.exec_()
        #self.app.quit()

    #def _on_load_finished(self):
    #    print(self.html)
    #    
    #    self.html = self.setContent(self.Callable)
    #    print('Load finished')

    #def Callable(self, html_str):
        #print(html_str)
    #    self.html = html_str
    #    self.app.quit()


def main():
    for x in [1]:
        page = Page('https://pythonprogramming.net/parsememcparseface/', QApplication(sys.argv))
        soup = bs.BeautifulSoup(page.html, 'html.parser')
        js_test = soup.find('p', class_='jstest')
        print(soup)

if __name__ == '__main__': main()