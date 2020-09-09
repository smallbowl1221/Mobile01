import os,csv

board_name = ["手機","相機","筆電","電腦","蘋果","影音","汽車","機車","單車","遊戲","居家","女性","時尚","運動","戶外","生活","旅遊美食","閒聊","時事"]


def creat(address,date):

    try:
        f = open(address + date + "_文章" + ".csv")
        f.close()

    except FileNotFoundError:
        with open(address + date + "_文章" + ".csv", "w", newline='',encoding="utf-8-sig") as csvFile:
            # 建立 CSV 檔寫入器
                writer = csv.writer(csvFile)
                #寫出-標題(first time)
                writer.writerow(['URL','公司','article_ID','回應數','版','標題','時間','內容'])

    try:
        f = open(address + date + "_回應" + ".csv")
        f.close()

    except FileNotFoundError:
        with open(address + date + "_回應" + ".csv", "w", newline='',encoding="utf-8-sig") as csvFile:
            # 建立 CSV 檔寫入器
                writer = csv.writer(csvFile)
                #寫出-標題(first time)
                writer.writerow(['URL','article_ID','樓層','名字','讚數','時間','回應內容'])