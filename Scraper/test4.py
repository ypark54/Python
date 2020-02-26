import bs4 as bs
import sys
import urllib.request
from queue import Queue
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl


class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print(self.html)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


def main():
    page = Page('https://www.3dmark.com/newsearch#advanced?test=spy%20P&cpuId=2403&gpuId=1310&gpuCount=0&deviceType=ALL&memoryChannels=0&country=&scoreType=overallScore&hofMode=false&showInvalidResults=false&freeParams=')
    soup = bs.BeautifulSoup(page.html, 'lxml')
    js_test = soup.find('div', class_='average-score')
    print(js_test)
    score = js_test.find('span', id='medianScore')
    print(score)

if __name__ == '__main__': main()