from selenium import webdriver
from lxml import etree
import csv

browser = webdriver.Chrome()
def get_page_source(url):
    try:
        browser.get(url)
        html = browser.page_source
        return html
    except:
        return None
    finally:
        browser.close()

def parse_html(html):
    item_list = []
    response = etree.HTML(html)
    tr_list = response.xpath("//div[@class='fht-fixed-body']//tbody/tr")[:10]
    for tr in tr_list:
        item = {}
        item['rank'] = tr.xpath("./td[1]/div[@class='rank']/text()")[0].strip()
        item['country'] = tr.xpath(".//div[@class='stub-name']/a/text()")[0].strip()
        item['2018'] = tr.xpath("./td[2]/text()")[0].strip()
        item['2017'] = tr.xpath("./td[3]/text()")[0].strip()
        item['2016'] = tr.xpath("./td[4]/text()")[0].strip()
        item['2015'] = tr.xpath("./td[5]/text()")[0].strip()
        item['2014'] = tr.xpath("./td[6]/text()")[0].strip()
        item['2013'] = tr.xpath("./td[7]/text()")[0].strip()
        item['2012'] = tr.xpath("./td[8]/text()")[0].strip()
        item['2011'] = tr.xpath("./td[9]/text()")[0].strip()
        item['2010'] = tr.xpath("./td[10]/text()")[0].strip()
        item_list.append(item)
    return item_list

def save_data(item_list):
    with open('E:/datas/pork_export.csv','w',encoding='utf-8') as f:
        fieldnames = ['rank','country','2018','2017','2016','2015','2014','2013','2012','2011','2010']
        writer = csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
        for item in item_list:
            writer.writerow(item)

if __name__ == '__main__':
    url = 'https://cn.knoema.com/atlas/topics/%e5%86%9c%e4%b8%9a/%e8%b4%b8%e6%98%93%e5%87%ba%e5%8f%a3%e9%87%8f/%e7%8c%aa%e8%82%89'
    html = get_page_source(url)
    item_list = parse_html(html)
    save_data(item_list)
    print('保存完毕')

