from everytime import Everytime

import time

my_id = input("id")
my_pw = input("pw")
MyET = Everytime()
print(MyET)
login_result = MyET.login(my_id, my_pw)
print(MyET.get_article_comment(102179408))
start = time.time()
for i in MyET.get_article_list(380299):
    print(i['article'])
    for j in i['comments']:
        print(j)
    print('------')
print(time.time()-start)
start = time.time()
# print(MyET.async_get_article_list(380299))
for i in MyET.async_get_article_list(380299):
    print(i['article']['created_at'])
    # for j in i['comments']:
    #     print(j)
    print('------')
print(time.time()-start)
