import os
#from decrypt import*
from encrypt import*
from cryptography.fernet import Fernet
import base64
import hashlib
import numpy as np
import string, random, time
import os
import shutil
import csv

def decrypt_data(data,password):
    size = int(data[-1:].decode())
    data = data[:-(size + 1)]    
    key = gen_fernet_key(password.encode('utf-8'))
    fernet = Fernet(key)
    decMessage = fernet.decrypt(data).decode()
    return decMessage

#Hàm đọc nội dung mã hóa được lưu ở nhiều file khác nhau
def readData(fileName):
    fileName = 'encr/'+fileName
    allData =b''
    f = open(fileName,'rb') 
    if f:
        data = f.read()
        allData += data[44:-10]
        while(len(data)>150):
            f = open(data[-10:].decode() + '.txt','rb')
            if f:
                data = f.read()
                if (len(data) > 150):
                    allData += data[:-10]
                else:
                    allData += data
    return allData    

#Hàm lấy mật khẩu động
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

#Hàm kiểm tra mật khẩu của 1 file đã mã hóa
def checkPassword(fileName, password):
    f = open('encr/' + fileName)
    data = f.read()
    data = data[0:44]
    if data.encode() == gen_fernet_key(password.encode('utf-8')):
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

#Hàm xóa tất cả file chứa nội dung mã hóa sau khi file đó được giải mã
def removeFile(fileName):
    fileName = 'encr/' + fileName
    file= open(fileName, 'r')
    data = file.read()
    nextFile = data[-10:]
    file.close()
    os.remove(fileName)
    while 1:
        try :
            file= open(nextFile + '.txt', 'r')
            data = file.read()
            file.close()
            os.remove(nextFile + '.txt')
            nextFile = data[-10:]
        except IOError:
            return

#Hàm tiến hành giải mã
def runDecrypt():
    fileName = input('Nhập tên file cần giải mã:')
    while checkFileExists('encr/',fileName) == False:
        fileName = input('File không tồn tại hoặc chưa được mã hóa. Nhập 0 để thoát hoặc nhập lại tên file: ')
        if fileName == 0: 
            return
    password = input('Nhập mật khẩu để mã hóa:')
    while checkPassword(fileName,password) == False:
        password = input('Mật khẩu sai. Nhấn 0 để thoát hoặc nhập lại: ')
        if password == '0':
            return

    OTP = input('Nhập mật khẩu động để tiếp tục: ')
    while checkPassDong(OTP) == False:
        OTP = input('Mật khẩu sai. Nhấn 0 để thoát hoặc nhập lại: ')
        if OTP == '0':
            return

    passmode = input('Nhập mật khẩu số để tiếp tục:')
    passMode(passmode)

    data = readData(fileName)
    de_data = decrypt_data(data,password)
    deFileName = input('Nhập tên file để lưu nọi dung giải mã:')
    while checkFileExists('',deFileName):
        deFileName = input('File đã tồn tại. Nhập 0 để thoát hoặc nhập lại tên file: ')
        if deFileName == 0: 
            return
    dencrypted_file = open(deFileName,'w')  
    dencrypted_file.write(de_data)
    dencrypted_file.close()
    removeFile(fileName)
    print('Giải mã thành công.')
