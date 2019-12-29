from et_fuction import Everytime

my_id = input("id")
my_pw = input("pw")
MyET = Everytime(my_id,my_pw)
login_result = MyET.login()
print(login_result)
vote_result = MyET.vote(451463515)
print(vote_result)