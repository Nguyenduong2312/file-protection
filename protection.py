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
    if realPassword == getPassDong(): 
        return True
    return False

#Hàm kiểm tra tổng 2 a,b mode cho n có bằng c hả không
def checkMode(a,b,c,n):
    return (a+b)%n == c

#Hàm kiểm tra mật khẩu 
def passMode(password):
    while len(password) != 7 or password[1:3] + password[4:6] != getPassDong():
        password = input('Mật khẩu không hợp lệ. Nhấn 0 để thoát hoặc nhập lại mật khẩu: ')
        if password == '0':
            return            
    n = int(password[0])
    for i in range(1, len(password), 3):
        while checkMode(int(password[i]),int(password[i+1]),int(password[i+2]),n) == False:
            password = input('Mật khẩu không hợp lệ. Nhấn 0 để thoát hoặc nhập lại mật khẩu: ')
            if password == '0':
                return

 #Hàm kiểm tra một ký tự có phải là chữ số hay không
def checkNumber(char):
    if ord(char) > 47 and ord(char) < 58:
        return True
    return False
#Hàm kiểm tra mật khẩu
def pass1(password):
    realPass = ''
    count = 0
    for i in range (0, len(password)):
        if password[i] == '0':
            realPass += '0'
            count = 0
        elif checkNumber(password[i]):
            count += 1
            if i == len(password) - 1:
                realPass += str(count)
        elif count != 0:
            realPass += str(count)
            count = 0
    return realPass

#Hàm kiểm tra mật khẩu 
def pass2(password):
    n = int(password[0])
    realPass = ''
    while len(password) > n+1:
        password = password[n + 1:]
        realPass += password[0]
    return realPass

