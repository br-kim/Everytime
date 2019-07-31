import et_fuction as ET
import requests
import sys
from bs4 import BeautifulSoup

my_id = input("아이디 입력 : ")
my_pw = input("비밀번호 입력 : ")
session = ET.login_request(my_id,my_pw)
choose = input("글을 지우시려면 1을, 댓글을 지우시려면 2를 입력해주세요.")
print("도중에 중지하시려면 CTRL + C 를 누르세요.")

def delete_article(session,target_id) :
    delete_article_url = "https://everytime.kr/remove/board/article"
    delete_article_body = {"id":target_id}
    delete_article_res = session.post(url=delete_article_url,data=delete_article_body,headers=ET.hdr)
    return delete_article_res
    
try :
    while choose == "1" :
        my_article_res = ET.get_my_article(session)
        soup = BeautifulSoup(my_article_res.text,"lxml")
        articles= soup.select("article")
        if articles == [] :
            print("더 이상 지울 글이 없습니다.")
            break
        for article in articles:
            sys.stdout.write(str(article['title'])+'\n')
            sys.stdout.write(str(article['text']).replace("<br />", "\n")+'\n')
            delete_article(session,article.get('id'))
            sys.stdout.write(str(article.get('id'))+' 삭제되었습니다.'+'\n')

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
                    print(comment['text'])
                    ET.delete_comment(session,comment['id'])
                    print(comment['id'],"삭제되었습니다.")
except KeyboardInterrupt :
    print("중지되었습니다.")

    