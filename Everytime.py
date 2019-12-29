import requests

class Everytime :

    hdr = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
            'Host' : 'everytime.kr',
            'Origin': 'https://everytime.kr',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://everytime.kr/',
            'DNT':'1',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

    def __init__(self,my_id,my_pwd):
        self.user_id = my_id
        self.user_pwd = my_pwd
        self.session = requests.session()
    
    def login(self) :
        url = 'https://everytime.kr/user/login'
        body = {'userid' :self.user_id, 'password': self.user_pwd,'redirect':'/'}
        response = self.session.post(url=url,data=body)
        if ('아이디나 비밀번호를 바르게 입력해주세요.' in response.text) :
            print("로그인 실패.")
        return response.text

    def vote(self,target,target_id) :
        """target = article or comment
        target_id = target's number
        """
        url = f'https://everytime.kr/save/board/{target}/vote'
        body = {'id':target_id,'vote':1}
        response = self.session.post(url=url,data=body,headers=self.hdr)
        return response.text

    def get_my_commented_article_list(self,start_num=0) : 
        url = 'https://everytime.kr/find/board/article/list'
        body = {'id':'mycommentarticle','limit_num':20,'start_num':start_num,'moiminfo':'true'}
        article_list_res = self.session.post(url=url,data=body,headers=self.hdr)
        return article_list_res

    #remove 
    def delete(self,target,target_id) :
        """target = article or comment
        target_id = target's number
        """
        url = f'https://everytime.kr/remove/board/{target}'
        body = {'id':target_id}
        delete_comment_res = self.session.post(url=url,data=body,headers=self.hdr)
        return delete_comment_res

def get_article_comment(session,target_id) : #target_id 글의 전체 내용과 댓글을 요청한다.
    article_comment_url = 'https://everytime.kr/find/board/comment/list'
    article_comment_body = {'id':target_id,'limit_num':-1,'moiminfo':'true'}
    article_comment_res = session.post(url=article_comment_url,data=article_comment_body,headers=self.hdr)
    return article_comment_res

def get_article_list(session,target_id,start_num=0) : #target_id 게시판의 글 목록을 요청한다.
    article_list_url = 'https://everytime.kr/find/board/article/list'
    article_list_body = {'id':target_id,'limit_num':20,'start_num':start_num,'moiminfo':'true'}
    article_list_res = session.post(url=article_list_url,data=article_list_body,headers=self.hdr)
    return article_list_res

def get_my_article(session,start_num=0) : #start_num 입력시 그 번호부터 20개 요청.
    my_article_url = 'https://everytime.kr/find/board/article/list'
    my_article_body = {'id' : 'myarticle', 'limit_num' : 20 , 'start_num' : start_num, 'moiminfo' : 'true'}
    my_article_res = session.post(url=my_article_url,data=my_article_body,headers=self.hdr)
    return my_article_res

#save
def write_article(session,title,text,target_id,anonym=1) : #기본으로 익명으로 작성,anonym=0 은 아이디 공개 작성
    write_url = 'https://everytime.kr/save/board/article'
    write_body = {'id':target_id,'text':text,'is_anonym':anonym,'title':title}
    write_res = session.post(url=write_url,data=write_body,headers=self.hdr)
    return write_res
