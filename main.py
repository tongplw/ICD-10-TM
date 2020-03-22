import requests
import lxml.html as lh
import pandas as pd
import threading

url = 'http://203.157.232.109/hdc_report/frontend/web/index.php?r=cicd10tm%2Findex&page='
data = []

START_PAGE = 1
STOP_PAGE = 2050
WINDOW = 100

def scrape(url):
    global data

    r = requests.get(url)
    doc = lh.fromstring(r.content)
    tr_elements = doc.xpath('//tr')

    for element in tr_elements[1:]:
        data += [[t.text_content() for t in element]]

def func(start, stop):
    for i in range(start, stop): #2042
        scrape(url + str(i))

        if i%10 == 0: print(i)

t = []
for i in range(START_PAGE, STOP_PAGE, WINDOW):
    x = threading.Thread(target=func, args=(i, i+WINDOW))
    x.start()
    t.append(x)

for i in t:
    i.join()

df = pd.DataFrame(data)
df.to_csv('icd.csv', encoding='utf-8-sig', index=False)