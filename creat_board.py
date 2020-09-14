import os,csv

board_name = ["手機","相機","筆電","電腦","蘋果","影音","汽車","機車","單車","遊戲","居家","女性","時尚","運動","戶外","生活","旅遊美食","閒聊","時事"]

#address 包含年
def creat(address,date):

    year = date[0:4]
    month = date[5:7]

    #檢查目錄是否存在
    if not os.path.isdir(address):
        #建立 年 dir
        os.mkdir(address)

        
        for m in range(1,13,1):

            if(len( str(m) ) < 2):
                m = "0" + str(m)

            #建立月資料夾
            os.mkdir(address + "\\" + str(m) + "月")

            #建立檔案年月
            ym = year + "_" + str(m)

            for i in board_name:
                #建立文章.csv檔案
                with open(address + "\\" + str(m) + "月" + "\\" + ym + "_" + i + "_文章" + ".csv", "w", newline='',encoding="utf-8-sig") as csvFile:
                    # 建立 CSV 檔寫入器
                        writer = csv.writer(csvFile)
                        #寫出-標題(first time)
                        writer.writerow(['URL','公司','article_ID','回應數','版','標題','時間','內容'])

                #建立回應.csv檔案
                with open(address + "\\" + str(m) + "月" + "\\" + ym + "_" + i +  "_回應" + ".csv", "w", newline='',encoding="utf-8-sig") as csvFile:
                    # 建立 CSV 檔寫入器
                        writer = csv.writer(csvFile)
                        #寫出-標題(first time)
                        writer.writerow(['URL','article_ID','樓層','名字','讚數','時間','回應內容'])

#region
    # try:
    #     f = open(address + date + "_文章" + ".csv")
    #     f.close()

    # except FileNotFoundError:
    #     with open(address + date + "_文章" + ".csv", "w", newline='',encoding="utf-8-sig") as csvFile:
    #         # 建立 CSV 檔寫入器
    #             writer = csv.writer(csvFile)
    #             #寫出-標題(first time)
    #             writer.writerow(['URL','公司','article_ID','回應數','版','標題','時間','內容'])

    # try:
    #     f = open(address + date + "_回應" + ".csv")
    #     f.close()

    # except FileNotFoundError:
    #     with open(address + date + "_回應" + ".csv", "w", newline='',encoding="utf-8-sig") as csvFile:
    #         # 建立 CSV 檔寫入器
    #             writer = csv.writer(csvFile)
    #             #寫出-標題(first time)
    #             writer.writerow(['URL','article_ID','樓層','名字','讚數','時間','回應內容'])
#endregion