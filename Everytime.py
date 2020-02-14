import requests
from bs4 import BeautifulSoup


def make_article_dict(article_obj):
    article = dict()
    article['title'] = article_obj.get('title')
    article['text'] = article_obj.get('text').replace("<br />", "\n")
    article['id'] = article_obj.get('id')
    article['posvote'] = article_obj.get('posvote')
    article['user_nickname'] = article_obj.get('user_nickname')
    article['created_at'] = article_obj.get('created_at')
    return article


def make_comment_dict(comment_objs):
    comments = []
    for comment_obj in comment_objs:
        comment = dict()
        if comment_obj.get('parent_id') == '0':
            comment['text'] = comment_obj.get('text')
        else:
            comment['text'] = 'ㄴ' + comment_obj.get('text')
        comment['created_at'] = comment_obj.get('created_at')
        comment['posvote'] = comment_obj.get('posvote')
        comment['user_nickname'] = comment_obj.get('user_nickname')
        comments.append(comment)
    return comments


class Everytime:
    hdr = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" 
        "Chrome/79.0.3945.88 Safari/537.36",
        'Host': 'everytime.kr',
        'Origin': 'https://everytime.kr',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://everytime.kr/',
        'DNT': '1',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    def __init__(self):
        self.session = requests.session()
        self.login_flag = False
        self.user_id = None

    def __str__(self):
        if self.login_flag:
            return f'{self.user_id} logged in session {self.session}'
        else:
            return 'not logged in session'

    def login(self, my_id, my_pwd):
        self.user_id = my_id
        url = 'https://everytime.kr/user/login'
        body = {'userid': self.user_id, 'password': my_pwd, 'redirect': '/'}
        response = self.session.post(url=url, data=body)
        if '아이디나 비밀번호를 바르게 입력해주세요.' in response.text:
            print("로그인 실패.")
            return None
        else:
            self.login_flag = True
            return response

    def vote(self, target, target_id):
        """target = article or comment
        target_id = target's number
        """
        url = f'https://api.everytime.kr/save/board/{target}/vote'
        body = {'id': target_id, 'vote': 1}
        response = self.session.post(url=url, data=body, headers=self.hdr)
        return response

    def get_my_commented_article_list(self, start_num=0):
        url = 'https://api.everytime.kr/find/board/article/list'
        body = {'id': 'mycommentarticle', 'limit_num': 20, 'start_num': start_num, 'moiminfo': 'true'}
        article_list_res = self.session.post(url=url, data=body, headers=self.hdr)
        return article_list_res

    # remove
    def delete(self, target, target_id):
        """target = 'article' or 'comment'
        target_id = target's number
        """
        url = f'https://api.everytime.kr/remove/board/{target}'
        body = {'id': target_id}
        delete_comment_res = self.session.post(url=url, data=body, headers=self.hdr)
        return delete_comment_res

    def get_article_comment(self, target_article_id):  # target_id 글의 전체 내용과 댓글을 요청한다.
        url = 'https://api.everytime.kr/find/board/comment/list'
        body = {'id': target_article_id, 'limit_num': -1, 'moiminfo': 'true'}
        article_comment_res = self.session.post(url=url, data=body, headers=self.hdr)
        soup = BeautifulSoup(article_comment_res.text, 'html.parser')
        # article id, title, created_at, posvote, user_nickname
        article_obj = soup.find('article')
        if article_obj:  # 해당 id의 글이 존재할 경우
            article = make_article_dict(article_obj)
            # comment id, parent_id(0 is root) text, created_at, posvote, user_nickname
            comment_objs = soup.find_all('comment')
            comments = make_comment_dict(comment_objs)
            return {'article': article, 'comments': comments}
        else:
            return "This article does not exist."

    def get_article_list(self, target_board_id,
                         start_num=0):  # target_id 게시판의 글 목록을 요청한다. #start_num 입력시 그 번호부터 20개 요청.
        """ target_id = target board's number or 'myarticle'(get My writing)
        """
        url = 'https://api.everytime.kr/find/board/article/list'
        body = {'id': target_board_id, 'limit_num': 20, 'start_num': start_num, 'moiminfo': 'true'}
        article_list_res = self.session.post(url=url, data=body, headers=self.hdr)
        soup = BeautifulSoup(article_list_res.text, 'html.parser')
        raw_all_article = soup.find_all("article")
        articles = []
        for article in raw_all_article:
            articles.append(self.get_article_comment(article.get('id')))
        return articles

    # save
    def write_article(self, text, target_id, title=None, anonym=1):  # 기본으로 익명으로 작성, anonym=0 은 아이디 공개 작성
        """ anonym : Writing anonymously => 1 Writing by name => 0 (default 1)
        writing on freeboard need 'title'
        'target_id' => board number
        """
        url = 'https://api.everytime.kr/save/board/article'
        body = None
        if title:  # 제목이 필요한 게시판
            body = {'id': target_id, 'text': text, 'is_anonym': anonym, 'title': title}
        else:
            body = {'id': target_id, 'text': text, 'is_anonym': anonym}

        write_res = self.session.post(url=url, data=body, headers=self.hdr)
        return write_res
