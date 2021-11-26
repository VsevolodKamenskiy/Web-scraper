import requests

from bs4 import BeautifulSoup

word = input()
url = input()
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
paragraphs = soup.find_all('p')

for p in paragraphs:
    if p.get_text().find(word) != -1:
        print(p.get_text())
