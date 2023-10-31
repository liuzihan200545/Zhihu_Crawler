"""
功能:爬取知乎收藏夹所有文章标题和链接
方法:Selenium + lxml + openpyxl
"""

import logging
from selenium import webdriver
from lxml import etree
import openpyxl
from threading import Thread

# Constants
COLLECTION_URL = "https://www.zhihu.com/collection/1234567"
PAGE_TEXT = "?page="

# Global vars
driver = None

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_page_html(url):
    try:
        driver.get(url)
        html = driver.page_source
        return etree.HTML(html)
    except Timeout:
        logging.error("Error getting page: %s", url)
        return None


def find_title(html):
    # 解析标题
    ...


def find_page_num(html):
    # 解析总页数
    ...


def main():
    global driver

    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    # 线程列表
    threads = []

    driver = webdriver.Edge()
    driver.get(COLLECTION_URL + PAGE_TEXT + "1")
    page_num = find_page_num(get_page_html(driver.current_url))

    for i in range(1, page_num + 1):
        t = Thread(target=crawl_page, args=[i])
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    workbook.save("collection.xlsx")


def crawl_page(page):
    url = COLLECTION_URL + PAGE_TEXT + str(page)
    html = get_page_html(url)
    if html:
        titles = find_title(html)
        logging.info("Crawled page %s", page)
    else:
        logging.error("Error crawling page %s", page)


if __name__ == "__main__":
    main()