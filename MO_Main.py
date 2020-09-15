import requests
import time,datetime
import bs4
import codecs
import os,sys
import csv
import string
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request as req
from fake_useragent import UserAgent

import creat_board
import MO_article_part

ua = UserAgent()

#紀錄執行時間
    #st = datetime.datetime.now()
    #start_time = st.strftime('%Y-%m-%d %H:%M:%S')

#抓取.csv的絕對路徑
Dir_address = os.path.abspath("..") + "\\Data\\Mobile\\M_Data"

#mobile主頁面
url_mobile = "https://www.mobile01.com/"

#board_name = ["手機","相機","筆電","電腦","蘋果","影音","汽車","機車","單車","遊戲","居家","女性","時尚","運動","戶外","生活","旅遊美食","閒聊","時事"]
#時事&閒聊 為 c
board_id = ["4","5","2","3","15","12","6","13","8","7","10","11","17","18","16","9","14","35","36"]

board_url_name = ["手機","相機","筆電","電腦","蘋果","影音","汽車","機車","單車","遊戲","居家","女性","時尚","運動","戶外","生活","旅遊美食","閒聊","時事"]
broad_url_c =["16","20","19","17","30","28","21","29","24","23","26","27","31","33","3","25","18","35","36"] 
broad_url = "https://www.mobile01.com/forumtopic.php?c="
#url = broad_url + broad_url[n]

# c = 目前第幾個版
# 由Mobile.bat餵的資料
# argv 為陣列[xxx.py , arg0 , arg1 , arg2 , ......]
# c = int(sys.argv[1])
c = 0
#印出目前版面
print(board_url_name[c] + ":")

article_url_list = []
article_response_num_list = []
article_date_list = []

#回應更新暫存(如有更新回應數)
#rs_index = [   ["文章編號","回應數量"] ]
rs_index = []

# 抓取網頁原始碼------------------------------------------------------------------------------------------------------------------
# run 1~20 page-------------------------------------------------------------------------------------------------------------------
for p in range(1,21):
    main_url = broad_url + broad_url_c[c] + "&p=" + str(p)
    request = req.Request(main_url, headers = {"User-Agent" : ua.chrome})
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    #取得文章bs4物件
    root = bs4.BeautifulSoup(data, "html.parser")

    #抓取每個版的每一頁文章列的html
    list_body = root.find("div",class_= "l-listTable__tbody")
    #抓取每個文章欄連結的html
    article_set = list_body.findAll("div",class_ = "c-listTableTd__title")
    #抓取每個文章欄回應數的html
    response_num_set = list_body.findAll("div",class_ = "l-listTable__td l-listTable__td--count")
    #抓取每個文章的時間
    time_set = list_body.findAll("div",class_ = "o-fNotes")

    #將每個文章的url存入article_url_list中(type:str)
    for i in article_set:
        article_url_list.append( url_mobile + i.a["href"] )
    #將每個文章的回應數存入article_response_num_list中(type:str)
    for j in response_num_set:
        article_response_num_list.append(j.div.text)
    #將每個文章的時間處理成 yyyy_mm
    for t in time_set:
        str_time = t.text[0:4] + "_" + t.text[5:7]
        article_date_list.append(str_time)



        

#逐一處理單一文章---------------------------------------------------------------------------------------------------------------
article_exist = False
for num in range(len(article_url_list)):
    print("-"*50)
        
    url = article_url_list[num]                 #單一文章url
    rs_num = article_response_num_list[num]     #單一文章回應數
    file_date = article_date_list[num]          #單一文章時間
    
    #將時間獨立出來
    year = file_date[0:4]
    month = file_date[5:7]

    #欲抓的文章id
    id_t = board_id[c] + "_" + url[url.find("t=")+2:url.find("t=")+9]

    #檢查新建 DATA path
    creat_board.creat(Dir_address + "\\" + year , file_date)

    #將資料位置加上     年份\月份\時間_版
    Data_address = Dir_address + "\\" + year + "\\" + month + "月" +"\\" + file_date + "_" +board_url_name[c]



    #載入.csv並記錄之前的URL & 回應數--------------------------------------
    with open(Data_address + "_文章" + ".csv", newline="",encoding="utf-8-sig") as csvFile:
        print("open the file : " + file_date + "_" + board_url_name[c] + "_文章" + ".csv")
        dic = csv.DictReader(csvFile)#將.csv轉成dictionary
        id_vector = []
        rs_vector = []
        for row in dic:
            id_vector.append(row["article_ID"]) #將所有"article_ID" 存入id_vector
            rs_vector.append(row["回應數"]) #將所有"回應數" 存入rs_vector

    #print(id_vector)
    #print(rs_vector)

    #檢查是否重複(article_exist = True ==> 文章存在)
    #i = 記錄中的index
    for i in range(len(id_vector)):
        if( id_t == id_vector[i]):
            article_exist = True
            #檢查現在文章回應數是否大於紀錄
            if(int(rs_num) > int(rs_vector[i])): 
                #儲存.csv紀錄中的回應數
                fr = int(rs_vector[i])
                rs_updata = True
            else:
                rs_updata = False
            break
        else:
            article_exist = False
            rs_updata = False
        
    #若沒有重複 ==> 新增資料
    if(not article_exist):
        print("首次寫入之文章: " + url )
        MO_article_part.getcontent(Data_address,url,id_t,int(rs_num))
        
    #若重複
    elif(rs_updata):

        # 標示處理之url
        print("更新回應之文章: " + url )

        #如果回應數比紀錄的多 ==> 更新回應
        MO_article_part.rs_updata(Data_address,url,file_date,id_t,fr)
            
        #更新該文章的回應數---------------------------------------------------------------------------------------------------------------
        with open( Data_address + "_文章" + ".csv" , newline="" , encoding="utf-8-sig" ) as csvFile:
            #用pandas讀取csv檔案
            df = pd.read_csv(csvFile)
            #index_col= "article_ID"
            df.loc[ df["article_ID"] == id_t,"回應數"] = rs_num
                            
            #將df(dataframe)更新CSV
            df.to_csv( Data_address + "_文章" + ".csv" ,index = False , encoding="utf-8-sig") 
        print( "更新之檔案/id/回應數: " + file_date + "_" +board_url_name[c] + ".csv" + " / " +  id_t + " / " + rs_num)
    
    else:
        print(rs_updata)
# tiem txt
    # et = datetime.datetime.now()
    # end_time = et.strftime('%Y-%m-%d %H:%M:%S')

    # s = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    # e = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    # exetime = e - s

    # with open(os.path.dirname(os.path.abspath(__file__)) + "\\" + "exetime.txt","a+") as exetxt:
    #     exetxt.write(board_url_name[c] + ": " + str(exetime)+"\n")

time.sleep(10)