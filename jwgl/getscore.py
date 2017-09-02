import requests
import hashlib
import pytesseract
import os
from io import BytesIO
from bs4 import BeautifulSoup
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from .models import Account, Stunum

url = 'http://223.2.10.23/cas/logon.action'
url2 = 'http://223.2.10.23/cas/genValidateCode'
url3 = 'http://223.2.10.23/frame/jw/teacherstudentmenu.jsp?menucode=JW1314'
url4 = 'http://223.2.10.23/student/xscj.stuckcj.jsp?menucode=JW130706'
url5 = 'http://223.2.10.23/jw/common/showYearTerm.action'
url6 = 'http://223.2.10.23/student/xscj.stuckcj_data.jsp'

photourl = 'http://223.2.10.123/jwgl/photos/rx20'

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\
/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}

header1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\
/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36', 'Referer': url3}

header2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\
/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36', 'Referer': url4}

s = requests.Session()

def md5(str):
    m = hashlib.md5()
    m.update(str.encode('utf-8'))
    return m.hexdigest()

def getStatus(username, pwd, yzm):
    data = {
        'username': username,
        'password': md5(md5(pwd) + md5(yzm)),
        'randnumber': yzm,
        'isPasswordPolicy': '1'
    }
    t = s.post(url, data, headers=header)
    return t.json()


def getResults(userCode):
    s.get(url3, headers=header)
    s.get(url4, headers=header1)

    data2 = {
        'sjxz': 'sjxz1',
        'ysyx': 'yxcj',
        'userCode': userCode,
        'xn1': '2017',
        'ysyxS': 'on',
        'sjxzS': 'on',
        'menucode_current': ''
    }

    f = s.post(url6, data2, headers=header2)

    soup = BeautifulSoup(f.text, 'html.parser')

    info = list()
    table = soup.find('div', group='group').find_all('div')
    for i in table:
        info.append(i.string.split('：')[1])

    term = list()
    a = soup.find_all('td', style='border: none;width:25%;')
    for i in a:
        term.append(i.string.split('：')[1])

    grade = list()
    num = 0
    tb = soup.find_all('table', style='clear:left;width:256mm;font-size:12px;')
    for i in tb:
        t = i.find('tbody').find_all('tr')
        for j in t:
            g = j.find_all('td')
            temp = list()
            temp.append(term[num])
            for k in g:
                if k.string == None:
                    temp.append('')
                else:
                    temp.append(k.string)
            grade.append(temp)
        num += 1

    return (info, grade)

def Verify():
    try:
        r = s.get(url2, headers = header)
        buff = BytesIO(r.content)
        im = Image.open(buff)
        im = im.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(im)
        im = enhancer.enhance(2)
        im = im.convert('1')
        vcode = pytesseract.image_to_string(im, config='-psm 3')
    except:
        vcode = ''
    return vcode

def getScorebyid(id):
    results = ''
    yzm = Verify()

    # 数据库获取一组随机账号密码
    account = Account.objects.order_by('?')[0]
    username = account.idnum
    password = account.pwd
    status = getStatus(username, password, yzm)

    # 验证码错误
    while(status['status'] == '401'):
        yzm = Verify()
        status = getStatus(username, password, yzm)

        # 密码错误
        while(status['status'] == '402'):
            Account.objects.filter(idnum = username).delete()
            account = Account.objects.order_by('?')[0]
            username = account.idnum
            password = account.pwd
            status = getStatus(username, password, yzm)

    try:
        userCode = Stunum.objects.get(idnum = id).stunum
        results = getResults(userCode)
    except:
        pass
    return results
