import time
from PIL import ImageGrab
COUNT=0

#GUI编程
import tkinter as tk
import tkinter.font as tf

def click():
    #截图功能 两点式截图
    pic = ImageGrab.grab((219,736,1716,1018))#4个坐标分别是旧x，旧y，新x，新y
    pic.save(r"C:\beofuse\SH.jpg")

    global COUNT
    COUNT=COUNT +1
    lab['text']='已经进行了'+str(COUNT)+'次翻译'

    #调用百度AI进行日语识别
    from aip import AipOcr

    APP_ID = '**********************************'
    API_KEY = '********************************'
    SECRET_KEY = '**************************' #请填写百度AI的用户名密码安全码

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()



    image = get_file_content(r'C:\beofuse\SH.jpg')
    options = {}
    options["language_type"] = "JAP"
    options["detect_language"] = "true"

    text=client.basicGeneral(image, options)

    lens=len(text['words_result'])  #关键参数：所要翻译文字的行数
    crr=''    #character_recognition_result 文字识别结果收入一个字符串
    for tem1 in range(0,lens): #下面的判断条件专用于PS3寒蝉鸣泣之时粹 如果是普通用途 请无视
        #if 'くらしの' not in text['words_result'][tem1]['words'] and 'しか长' not in text['words_result'][tem1]['words'] and '●●'not in text['words_result'][tem1]['words'] and '。。' not in text['words_result'][tem1]['words'] and 'くらしく' not in text['words_result'][tem1]['words']:
        crr=crr+text['words_result'][tem1]['words']




#####################################################
    #调用百度翻译api
    # coding=utf-8

    import http.client
    import hashlib
    import urllib
    import random
    import json

    tah=''     #translation results here

    appid = '******************' 
    secretKey = '**************'          #请填写百度翻译api的用户名密码 

    httpClient = None
    myurl = '/api/trans/vip/translate'

    fromLang = 'jp'        #原文语种
    toLang = 'zh'           #译文语种
    salt = random.randint(32768, 65536)
    q= crr
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
    salt) + '&sign=' + sign
    
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        tah=result['trans_result'][0]['dst'].replace('标记', ' ')     #.replace('标记', ' ')专用于PS3寒蝉鸣泣之时粹 如果是普通用途 请删去


    except Exception as e:
        print (e)
    finally:
        if httpClient:
            httpClient.close()

    yw.delete(0.0, 'end')
    fy.delete(0.0, 'end')
    yw.insert('end',crr+'\n')
    fy.insert('end',tah+'\n')



top=tk.Tk()
top.wm_attributes('-topmost',1)                                        #窗口置顶
top.geometry('250x500')                                                   #窗口默认大小设置
top.title("基于百度AI和百度翻译的屏幕文字实时翻译软件")     #窗口名
ft = tf.Font(family='微软雅黑', size=8)                                #提醒框文字字体设置
ft1 = tf.Font(family='微软雅黑', size=12)                            #文本框文字字体设置

bt=tk.Button(text='进行截图翻译',command=click)
bt.pack()
yw=tk.Text(top,width=40,height=10,font=ft1)     #原文
yw.pack()
fy=tk.Text(top,width=40,height=10,font=ft1)      #译文
fy.pack()
lab=tk.Label(top,text='已经进行了0次翻译',compound='left',font=ft)
lab.pack()


top.mainloop()