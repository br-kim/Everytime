import et_fuction as ET
import requests
from bs4 import BeautifulSoup

my_id = input('아이디 입력 : ')
my_pw = input('비밀번호 입력 : ')
session = ET.login_request(my_id,my_pw)
my_article_res = ET.get_my_article(session)
html = my_article_res.text
soup = BeautifulSoup(html,'lxml')
articles = soup.find_all('article')
for article in articles :
    print('제목 : ',article['title'])
    print('내용 : ',article['text'].replace("<br />","\n"))
    print('------------------------')