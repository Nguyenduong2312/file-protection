import os
from encrypt import*
from protection import *
from cryptography.fernet import Fernet
import os

def decrypt_data(data,password):
    size = int(data[-1:].decode())
    data = data[:-(size + 1)]    
    print(type(data), data)
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

#Hàm kiểm tra mật khẩu của 1 file đã mã hóa
def checkPassword(fileName, password):
    f = open('encr/' + fileName)
    data = f.read()
    data = data[0:44]
    if data.encode() == gen_fernet_key(password.encode('utf-8')):
        return True
    return False

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


def runDecrypt1():
    fileName = input('Nhập tên file cần giải mã:')
    while checkFileExists('encr/',fileName) == False:
        fileName = input('File không tồn tại hoặc chưa được mã hóa. Nhập 0 để thoát hoặc nhập lại tên file: ')
        if fileName == 0: 
            return

    password = input('Nhập mật khẩu 1 để mã hóa:')
    while pass1(password) != getPassDong():
        password = input('Mật khẩu sai. Nhấn 0 để thoát hoặc nhập lại: ')
        if password == '0':
            return

    password = input('Nhập mật khẩu 2 để mã hóa:')
    while checkPassword(fileName,pass2(password)) == False:
        password = input('Mật khẩu sai. Nhấn 0 để thoát hoặc nhập lại: ')
        if password == '0':
            return
    passmode = input('Nhập mật khẩu số để tiếp tục:')
    passMode(passmode)
    data = readData(fileName)
    de_data = decrypt_data(data,pass2(password))
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
