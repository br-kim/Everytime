import et_fuction as ET
import requests
import sys
from bs4 import BeautifulSoup

def fast_print(*x) :
    sys.stdout.write(" ".join(list(map(str,x)))+"\n")

def validate_input() :
    while True:
        x = input("""글을 지우시려면 1을, 댓글을 지우시려면 2를 입력해주세요.
도중에 중지하시려면 CTRL + C 를 누르세요.""")
        if (x == "1") or (x =="2"):
            break
        else:
            print("다시 입력해주세요.")
            continue
    return x

my_id = input("아이디 입력 : ")
my_pw = input("비밀번호 입력 : ")
session = ET.login_request(my_id,my_pw)
choose= validate_input()
try :
    while choose == "1" :
        my_article_res = ET.get_my_article(session)
        soup = BeautifulSoup(my_article_res.text,"lxml")
        articles= soup.select("article")
        if articles == [] :
            print("더 이상 지울 글이 없습니다.")
            break
        for article in articles:
            fast_print(article['title'])
            fast_print(article['text'].replace("<br />", "\n"))
            ET.delete_article(session,article.get('id'))
            fast_print(article.get('id')+' 삭제되었습니다.')

    while choose == "2" :
        my_comment_res = ET.get_my_commented_article_list(session)
        soup = BeautifulSoup(my_comment_res.text,"lxml")
        articles = soup.select("article")
        if articles == []:
            print("더 이상 지울 댓글이 없습니다.")
            break
        for article in articles :
            entire_article_res = ET.get_article_comment(session,article.get('id'))
            soup2 = BeautifulSoup(entire_article_res.text,"lxml")
            comments = soup2.find_all("comment")
            for comment in comments :
                if(comment["is_mine"] == "1"):
                    fast_print(comment['text'])
                    ET.delete_comment(session,comment['id'])
                    fast_print(comment['id']+"삭제되었습니다.")
except KeyboardInterrupt :
    print("중지되었습니다.")