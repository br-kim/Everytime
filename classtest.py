from everytime import Everytime

my_id = input("id")
my_pw = input("pw")
MyET = Everytime(my_id,my_pw)
print(MyET)
login_result = MyET.login()
print(MyET)
print(login_result)