from everytime import Everytime

my_id = input("id")
my_pw = input("pw")
MyET = Everytime()
print(MyET)
login_result = MyET.login(my_id, my_pw)
#print(MyET.get_article_list(380299))
print(MyET.get_article_comment(102179408))
# for i in MyET.get_article_list(380299):
#     print(i)