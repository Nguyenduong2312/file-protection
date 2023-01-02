import os
from cryptography.fernet import Fernet
import base64
import hashlib
import numpy as np
import string, random, time
import os

def gen_fernet_key(passcode:bytes) -> bytes:
    assert isinstance(passcode, bytes)
    hlib = hashlib.md5()
    hlib.update(passcode)
    return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def encrypt_data(data,password):
    key = gen_fernet_key(password.encode('utf-8'))
    fernet = Fernet(key)
    encMessage = fernet.encrypt(data.encode())
    print('data en:',encMessage)
    extraByte = get_random_string(np.random.randint(1,10)).encode('utf-8')
    add = encMessage + extraByte + str(len(extraByte)).encode('utf-8')
    print('eta',extraByte)
    print('tong',add)
    return add

#Hàm trả về ngẫu nhiên tên tất 1 folder
def getFolderName():
    arr = os.listdir()
    list_folder = []
    for items in arr:
        if '.' not in items and items != '__pycache__':
            list_folder.append(items)
    return list_folder[np.random.randint(0,len(list_folder))]

#Hàm sinh ngẫu nhiên tên file có 5 ký tự (VD:ahdns.txt)
def generateFileName():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(5))
    return getFolderName() + '/' + result_str + ".txt"

#Hàm ghi dữ liệu vào nhiều file khác nhau, mỗi file chứa 150 ký tự. Các file được lưu vào folder encr
#File ghi 150 ký tự đầu có tên do người dùng nhập vào
#Các file sau có tên do chương trình random và được lưu vào cuối nội dung file trước đó
#Cách làm này tương tự như Danh sách liên kết
def writeData(fileName,data):
    fileName = "encr/" + fileName
    with open(fileName, 'ab+') as encrypted_file:
        if len(data) <= 150:
            encrypted_file.write(data[0:len(data)])
            return 
        encrypted_file.write(data[0:150])
        newFile = generateFileName().encode()
        encrypted_file.write(newFile[:-4])
        newFile =newFile.decode()
        # tạo file mới có tên random
    data = data[150:] #xóa 150 byte đầu của data
    while (len(data) / 150 > 1):
        with open(newFile, 'ab+') as encrypted_file:
            encrypted_file.write(data[0:150])
            newFile = generateFileName().encode()
            encrypted_file.write(newFile[:-4])
            newFile =newFile.decode()
        data = data[150:] #xóa 150 byte đầu của data
    with open(newFile, 'ab+') as encrypted_file:
        encrypted_file.write(data)

#Hàm mã hóa file với password được cung cấp
def encrypt(fileName,enFileName,password):
    while 1:
        try:
            file= open(fileName, 'r')
        except IOError:
            fileName = input("Khong the mo file nhan 0 de thoat, hoac nhap ten file moi: ")
            if (fileName == '0'):
                return
        data = file.read()
        key = gen_fernet_key(password.encode('utf-8')) 
        encrypted = key + encrypt_data(data,password)
        print('en:',encrypted)
        #hàm ghi data vào nhiều file
        writeData(enFileName,encrypted)
        return

#Hàm kiểm tra một file có được mã hóa chưa 
def checkFileExists(direct,fileName):
    try :
        open(direct + fileName)        
        return True
    except IOError:
        return False

#Hàm tiến hành mã hóa
def runEncrypt():
    fileName = input('Nhập tên file cần mã hóa:')
    enFileName = input('Nhập tên file lưu dữ liệu mã hóa:')
    while checkFileExists('encr',enFileName):
        enFileName = input('Tên file đã tồn tại,nhập 0 để thoát hoặc nhập tên mới:')
        if enFileName == 0 :
            return
    password = input('Nhập mật khẩu để mã hóa file:')
    encrypt(fileName,enFileName,password)

