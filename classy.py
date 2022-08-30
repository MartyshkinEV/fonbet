
class Requet:
    cate=[]


    def __init__(self):
        from configur import url_1
        import requests
        import os
        import json

        try:
            os.remove('json.txt')
        except:
            pass
        resp=requests.get(url_1)
        j_resp=resp.json()

        with open('json.txt','w') as outfile:
            json.dump(j_resp, outfile)
        print("Requet успешно завершил работу!")


class Jsn_txt:
    cate=''


    def __init__(self, categ):
        import json
        f = open('json.txt', 'r')  # открыли файл
        text = json.load(f)  # загнали все из файла в переменную
        catet=(text[categ])
        self.cate=catet
        print(' параметр cate готов')



class Tims:
    ts_nw=''
    def __init__(self):
        import time
        print('определяется время')
        ts_now = time.time()
        ts_now = (round(ts_now))

        self.ts_nw=ts_now

























