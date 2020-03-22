import requests
import lxml.html as lh
import pandas as pd
import threading

# url = 'http://203.157.232.109/hdc_report/frontend/web/index.php?r=cicd10tm%2Findex&page=1'
url = 'http://61.7.219.187/datacheck/frontend/web/index.php?r=icd10%2Findex&page='


START_PAGE = 1
STOP_PAGE = 500 #2137
WINDOW = 50

def scrape(url):
    global data

    r = requests.get(url)
    doc = lh.fromstring(r.content.decode('UTF-8'))
    tr_elements = doc.xpath('//tr')

    for element in tr_elements[1:]:
        data += [[t.text_content() for t in element]]

def func(start, stop):
    for i in range(start, stop): #2042
        scrape(url + str(i))

        if i%10 == 0: print(i)

data = []
t = []
for i in range(START_PAGE, STOP_PAGE, WINDOW):
    x = threading.Thread(target=func, args=(i, i+WINDOW))
    x.start()
    t.append(x)

for i in t:
    i.join()

df = pd.DataFrame(data)
df.to_csv('output.csv', encoding='utf-8-sig', index=False)