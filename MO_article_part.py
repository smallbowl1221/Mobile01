import requests
import re
import time
import xml
import bs4
import codecs
from fake_useragent import UserAgent
import os
import csv
import string
from bs4 import BeautifulSoup
import urllib.request as req

# addr = os.path.dirname(os.path.abspath(__file__)) + "\\Data\\"

main_url = "https://www.mobile01.com/"

ua = UserAgent()    #random ua

#寫回回應csv
def write_csv(article_board ,rs_exist , address , url, id_t , response_list):
    #文章存入 回應之 CSV 檔案-------------------------------------------------------------------------------------------------------------------------------------------
        name_response_csv = article_board + "_回應.csv"  

        #確定有回應
        if(rs_exist):
            with open(address + name_response_csv, "a+", newline='',encoding="utf-8-sig") as csvFile:
                # 建立 CSV 檔寫入器
                writer = csv.writer(csvFile)
                
                #標題 ==> ['URL','article_ID','樓層','名字','讚數','時間','回應內容']
                #寫出-資料
                for rl in response_list:
                    writer.writerow([url,id_t,rl[0],rl[1],rl[2],rl[3],rl[4]])

#處理回應內容 回傳(list response_list, int fr)
def getresponse( response_set , fr):
    response_list = []
    for num in response_set:
        #name ---------------------------------------------------------
        name_set = num.find("div",class_ = "c-authorInfo__id")
        #消除空格
        name_reg = "".join(name_set.a.text.split())
         
        #樓層和時間-----------------------------------------------------
        #tf_set[0 ==> 時間 , 1 ==> 樓層]
        tf_set = num.find_all("span",class_ = "o-fNotes o-fSubMini")
        #時間
        t = str(tf_set[0].text)
        time_reg = t[0:4] + "年" + t[5:7] + "月" + t[8:10] + "日" + " " + t[11:16]  ##yyyy年mm月dd日 hh:mm

        #樓層
        if(tf_set[1].text[0] == "#"):
            floor_reg = tf_set[1].text
        else:
            floor_reg = "#1"  
        
        #like----------------------------------------------------------
        like_set =  num.find("label",class_ = "c-tool__check toolclap")
        like_reg = like_set.span.text
         
        #response content ---------------------------------------------
        response_set =  num.find("article",class_ = "u-gapBottom--max c-articleLimit")
        if(response_set != None):
            #去除子標籤的text
            response_set = response_set.find_all(text=True,recursive=False)
            article_response = "".join(response_set)
            #處理掉內容強行換行(改成不換行)
            article_response = article_response.split()
            article_response = "".join(article_response)
            # print(article_response)
        else:
            article_response = "Null"
  
        A_response = [floor_reg , name_reg , like_reg , time_reg , article_response ]
        response_list.append(A_response)
    fr += len(response_list)
    return(response_list,fr)
    #get response_list

#getcontent(位置 , url , 文章id , 回應數) :
def getcontent(address , url , id_t , fr1) :

    # 抓取網頁原始碼---------------------------------------------------------------------------------------------------------------------------------------
        request = req.Request(url, headers ={"User-Agent" : ua.chrome })    #ua.chrome ==> 隨機生成chrome的UserAgent
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")

    # 取得文章bs4物件-----------------------------------------------------------------------------------------------------------------------------------------
        root = bs4.BeautifulSoup(data, "html.parser")
    
    # 將原始碼存入txt中------------------------------------------------------------------------------------------------------------------------------------
        # with open("html.txt","w",encoding="utf-8") as fuck:
        #     fuck.write(str(root.prettify()))
        #     fuck.close()

    # 抓出版--------------------------------------------------------------------------------------------------------------------------------------------------
        article_board_set = root.find_all("li",class_ = "c-breadCrumb__item")
        article_board = article_board_set[1].a.text
        article_board = article_board.split()   #去除空格
        article_board = article_board[0]

    # 抓出標題-------------------------------------------------------------------------------------------------------------------------------------------------
        article_title_set = root.find_all("h1",class_ = "t2")
        article_title = str(article_title_set[0].text)

    # 抓出時間-------------------------------------------------------------------------------------------------------------------------------------------------
        article_time_set = root.find_all("span",class_ = "o-fNotes o-fSubMini")   #yyyy-mm-dd hh:mm
        #時間格式化
        t = str(article_time_set[0].text)
        article_time = t[0:4] + "年" + t[5:7] + "月" + t[8:10] + "日" + " " + t[11:16]  ##yyyy年mm月dd日 hh:mm

    # 文章內容------------------------------------------------------------------------------------------------------------------------------------------------

        # 搜尋出 "div" 且 itemprop = "articleBody" 的資料
        article_content_set = root.find_all("div", itemprop = "articleBody")
        # content_set 為一set格式
        article_content = str(article_content_set[0].text)

        #消除不必要的空行或換行
        article_content = article_content.split()
        article_content = "".join(article_content)
        
    # 文章回復處理--------------------------------------------------------------------------------------------------------------------------------------------------
        #fr => 回應數
        fr = 0

        response_list = []
        #抓取個回應的html
        response_set = root.find_all("div",class_ = "l-articlePage")
        
        
        #第一筆為文章
        del(response_set[0])

        #確定有回應
        if(len(response_set) > 0):
            #抓全部回應頁面
            rs_exist = True

            response_list,fr = getresponse(response_set, fr)
            write_csv(article_board , rs_exist , address , url , id_t , response_list)
            #確定有超過一頁的回應頁面
            try:
                totalnum = int(root.find_all("a",class_ = "c-pagination")[-1].text)
                for i in range(2,totalnum+1):
                    page_url = url + "&p=" + str(i)                                                         
                    request = req.Request(page_url, headers ={"User-Agent" : ua.chrome })
                    with req.urlopen(request) as response:                    
                        data = response.read().decode("utf-8")
                    page_reg = bs4.BeautifulSoup(data, "html.parser")
                    page_set = page_reg.find_all("div",class_ = "l-articlePage")#抓取回應html
                    del(page_set[0])    #刪除第一筆資料(非回應)
                    #呼叫 function getresponse( list page_set )
                    response_list,fr = getresponse( page_set , fr )
                    #print(len(response_list))
                    write_csv(article_board , rs_exist , address , url , id_t , response_list)
                print(url)
            except IndexError:
                print(url + "   :  no page")
        #2-1
            for num in response_set:
                #name ---------------------------------------------------------
                name_set = num.find("div",class_ = "c-authorInfo__id")
                #消除空格
                name_reg = "".join(name_set.a.text.split())

                #樓層和時間-----------------------------------------------------
                #tf_set[0 ==> 時間 , 1 ==> 樓層]
                tf_set = num.find_all("span",class_ = "o-fNotes o-fSubMini")
                #時間
                t = str(tf_set[0].text)
                time_reg = t[0:4] + "年" + t[5:7] + "月" + t[8:10] + "日" + " " + t[11:16]  ##yyyy年mm月dd日 hh:mm
            
                #樓層
                if(tf_set[1].text[0] == "#"):
                    floor_reg = tf_set[1].text
                else:
                    floor_reg = "#1"

                #like----------------------------------------------------------
                like_set =  num.find("label",class_ = "c-tool__check toolclap")
                like_reg = like_set.span.text

                #response content ---------------------------------------------
                response_set =  num.find("article",class_ = "u-gapBottom--max c-articleLimit")
                if(response_set != None):
                    #去除子標籤的text
                    response_set = response_set.find_all(text=True,recursive=False)
                    article_response = "".join(response_set)
                    #處理掉內容強行換行(改成不換行)
                    article_response = article_response.split()
                    article_response = "".join(article_response)
                    # print(article_response)
                else:
                    article_response = "Null"
                
                A_response = [floor_reg , name_reg , like_reg , time_reg , article_response ]
                response_list.append(A_response)

            del(response_list[0])
            #get response_list

        else:
            print("not response")

        print("fr1 = " + str(fr1))
        print("fr  = "+ str(fr))

    #文章存入 CSV 檔案--------------------------------------------------------------------------------------------------------------------------------------------
        name_csv = article_board + ".csv"

        with open(address + name_csv, "a+", newline='',encoding="utf-8-sig") as csvFile:
        # 建立 CSV 檔寫入器
            writer = csv.writer(csvFile)
            #標題 ==> ['URL','公司','article_ID','回應數','版','標題','時間','內容']
            #寫出-資料
            writer.writerow([url,"Mobile01",id_t,fr,article_board,article_title,article_time,article_content])

#rs_updata(位置,url,版名,文章id,回應數)
def rs_updata( address , url , article_board , id_t , fr ):
    # 標示處理之url------------------------------------------------------------------------------------------------------------------------------------------
        print("rs: " + url )

    # 抓取網頁原始碼-----------------------------------------------------------------------------------------------------------------------------------------
        request = req.Request(url, headers ={"User-Agent" : ua.chrome})
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")

    # 取得文章bs4物件-----------------------------------------------------------------------------------------------------------------------------------------
        root = bs4.BeautifulSoup(data, "html.parser")

        #確定有超過一頁的回應
        try:
            #抓取總共頁數
            totalnum = int(root.find_all("a",class_ = "c-pagination")[-1].text)
            
            #處理原先存取之回應數(抓取頁數及位置 p => 第幾頁  l => 第幾個回應)
            position = fr%10
            if( position != 0 ):
                p = int(fr/10)+1
            else:
                p = int(fr/10)
                position = 10
            
            #抓回應 p~totalnum 頁的URL
            for i in range(p,totalnum+1):
                page_url = url + "&p=" + str(i)
                request = req.Request(page_url, headers ={"User-Agent" : ua.chrome})
                with req.urlopen(request) as response:
                    data = response.read().decode("utf-8")
                page_reg = bs4.BeautifulSoup(data, "html.parser")
                page_set = page_reg.find_all("div",class_ = "l-articlePage")#抓取回應html
                del(page_set[0])    #刪除第一筆資料(非回應)
                print("page:" + str(i))
                #將第一個抓取的頁面依position來做塞選
                if(position != 0):
                    for j in range(position+1):
                        del(page_set[0])
                print("this page need response number : " + str( len(page_set) ) )
                #呼叫 function getresponse( list page_set )
                response_list,fr = getresponse( page_set , fr )
                #print(len(response_list))
                write_csv(article_board , True , address , url , id_t , response_list)
                #重設position
                position = 0
        except IndexError:
            print("nopage")
    



#getcontent("D:\python\crawler_NCU\\" , "https://www.mobile01.com/topicdetail.php?f=291&t=4369995" , "123" , 19500)
#rs_updata( "D:\python\crawler_NCU\\" , "https://www.mobile01.com/topicdetail.php?f=291&t=4369995" , "fuck" , "123" , 19501 )