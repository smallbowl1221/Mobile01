import os,csv

board_name = ["手機","相機","筆電","電腦","蘋果","影音","汽車","機車","單車","遊戲","居家","女性","時尚","運動","戶外","生活","旅遊美食","閒聊","時事"]

# s =[["1","2","3"],
    #     ["4","5","6"],
    #     ["7","8","9"]]

def creat(address):
    for i in board_name:
        try:
            f = open(address + i + ".csv")
            f.close()
            #print(i + ".csv" + "  exist")

        except FileNotFoundError:

            with open(address + i + ".csv", "w", newline='',encoding="utf-8-sig") as csvFile:
                # 建立 CSV 檔寫入器
                    writer = csv.writer(csvFile)
                    #寫出-標題(first time)
                    writer.writerow(['URL','公司','article_ID','回應數','版','標題','時間','內容'])

        try:
            f = open(address + i + "_回應" + ".csv")
            f.close()
            #print( i + "_回應" + ".csv" + "  exist")

        except FileNotFoundError:

            with open(address + i + "_回應" + ".csv", "w", newline='',encoding="utf-8-sig") as csvFile:
                # 建立 CSV 檔寫入器
                    writer = csv.writer(csvFile)
                    #寫出-標題(first time)
                    writer.writerow(['URL','article_ID','樓層','名字','讚數','時間','回應內容'])


