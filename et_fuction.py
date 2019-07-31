import requests

hdr = {'User-Agent': 
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
' (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
'Host' : 'everytime.kr',
'Origin': 'https://everytime.kr',
'X-Requested-With': 'XMLHttpRequest'
}

#login
def login_request(my_id,my_pw) :
    login_url = 'https://everytime.kr/user/login'
    login_session = requests.session()
    login_body = {'userid' :my_id, 'password': my_pw,'redirect':'/'}
    login_session.post(url=login_url,data=login_body)
    return login_session

#find
def get_my_commented_article_list(session,start_num=0) :
    article_list_url = 'https://everytime.kr/find/board/article/list'
    article_list_body = {'id':'mycommentarticle','limit_num':20,'start_num':start_num,'moiminfo':'true'}
    article_list_res = session.post(url=article_list_url,data=article_list_body,headers=hdr)
    return article_list_res

def get_article_comment(session,target_id) : #target_id 글의 전체 내용과 댓글을 요청한다.
    article_comment_url = 'https://everytime.kr/find/board/comment/list'
    article_comment_body = {'id':target_id,'limit_num':-1,'moiminfo':'true'}
    article_comment_res = session.post(url=article_comment_url,data=article_comment_body,headers=hdr)
    return article_comment_res

def get_article_list(session,target_id,start_num=0) : #target_id 게시판의 글 목록을 요청한다.
    article_list_url = 'https://everytime.kr/find/board/article/list'
    article_list_body = {'id':target_id,'limit_num':20,'start_num':start_num,'moiminfo':'true'}
    article_list_res = session.post(url=article_list_url,data=article_list_body,headers=hdr)
    return article_list_res

def get_my_article(session,start_num=0) : #start_num 입력시 그 번호부터 20개 요청.
    my_article_url = 'https://everytime.kr/find/board/article/list'
    my_article_body = {'id' : 'myarticle', 'limit_num' : 20 , 'start_num' : start_num, 'moiminfo' : 'true'}
    my_article_res = session.post(url=my_article_url,data=my_article_body,headers=hdr)
    return my_article_res

#save
def write_article(session,title,text,target_id,anonym=1) : #기본으로 익명으로 작성,anonym=0 은 아이디 공개 작성
    write_url = 'https://everytime.kr/save/board/article'
    write_body = {'id':target_id,'text':text,'is_anonym':anonym,'title':title}
    write_res = session.post(url=write_url,data=write_body,headers=hdr)
    return write_res

def vote_article(session,target_id) :
    vote_article_url = 'https://everytime.kr/save/board/comment/vote'
    vote_article_body = {'id':target_id,'vote':1}
    vote_article_res = session.post(url=vote_article_url,data=vote_article_body,headers=hdr)
    return vote_article_res

#remove 
def delete_comment(session,target_id) : 
    delete_comment_url = 'https://everytime.kr/remove/board/comment'
    delete_comment_body = {'id':target_id}
    delete_comment_res = session.post(url=delete_comment_url,data=delete_comment_body,headers=hdr)
    return delete_comment_res