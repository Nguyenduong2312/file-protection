#Hàm lấy mật khẩu động
import time
def getPassDong():
    t = time.localtime()
    return time.strftime("%H", t) + time.strftime("%M", t)

#hàm kiểm tra mật khẩu động
## password  = 3 ký từ đầu ngẫu nhiên + giờ(24h)(2 ký tự) + 1 dãy ký tự ngẫu nhiên + phút(2 ký tự) + 3 ký tự ngẫu nhiên
def checkPassDong(password): 
    password = password[:-3]
    realPassword = password[3:5] + password[-2:]
    print(realPassword , getPassDong())
    if realPassword == getPassDong(): 
        return True
    return False

#----
def checkMode(a,b,c,n):
    return (a+b)%n == c

def passMode(password):
    while len(password) % 3 != 1:
        password = input('Mật khẩu không hợp lệ. Nhấn 0 để thoát hoặc nhập lại mật khẩu: ')
        if password == '0':
            return
    n = int(password[0])
    for i in range(1, len(password), 3):
        while checkMode(int(password[i]),int(password[i+1]),int(password[i+2]),n) == False:
            password = input('Mật khẩu không hợp lệ. Nhấn 0 để thoát hoặc nhập lại mật khẩu: ')
            if password == '0':
                return

