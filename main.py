import re
from selenium import webdriver
from lxml import etree
import openpyxl

Collection_url = "https://www.zhihu.com/collection/769453471"
page_text = "?page="

def GetPageHeml(driver):
    html = driver.page_source
    html = etree.HTML(html)
    return html

def FindTitle(html):
    titles = html.xpath('//a[@data-za-detail-view-element_name="Title"]')
    list = []
    pattern = r'>(.*)</a>'
    for t in titles:
        d = etree.tostring(t,encoding='utf8').decode('utf8')
        d = re.findall(pattern,d)[0]
        list.append(d)
    return list

def FindPageNum(html):
    num_text = html.xpath('//button[@type="button"][5]')
    num_text = etree.tostring(num_text[0], encoding='utf8').decode('utf8')
    pattern = r'">(.*)</button>'
    num = int(re.findall(pattern,num_text)[0])
    return num

def FindUrl(html):
    urls = html.xpath('//a[@data-za-detail-view-element_name="Title"]')
    pattern = r'href="(.*?)"'
    list = []
    for url in urls:
        url = etree.tostring(url, encoding='utf8').decode('utf8')
        url = re.findall(pattern,url)[0]
        list.append(url)
    return list

if __name__ == "__main__":
    N = 1
    # 创建Excel工作簿
    workbook = openpyxl.Workbook()
    # 获取当前活动工作表
    worksheet = workbook.active
    driver = webdriver.Edge()
    driver.get(Collection_url + page_text + "1")
    result = GetPageHeml(driver)
    page_num = FindPageNum(result)
    for i in range(1,page_num+1):
        driver.get(Collection_url + page_text + str(i))
        html = GetPageHeml(driver)
        print(i)
        ans = FindTitle(html)
        while(True):
            if(len(ans)==0):
                driver.get(Collection_url + page_text + str(i))
                html = GetPageHeml(driver)
                ans = FindTitle(html)
            else:
                break
        urls = FindUrl(html)
        for j in range(len(ans)):
            print(ans[j])
            # 向工作表写入数据
            worksheet['A'+str(N)] = ans[j]
            worksheet['B'+str(N)] = urls[j]
            N += 1

    # 保存工作簿至本地
    workbook.save('example1.xlsx')





