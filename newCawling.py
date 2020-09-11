import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

RESULT_PATH = 'C:/Ddump/'  # 본인 파일 저장 위치로 변경
now = datetime.now()  # 파일이름 현 시간으로 저장하기


def get_news(n_url):
    news_detail = []

    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    breq = requests.get(n_url, headers=header)
    breq.encoding = 'utf8'
    bsoup = BeautifulSoup(breq.text, 'html.parser')

    title = bsoup.find_all('h1#news_title_text_id')[0].text
    news_detail.append(title)

    pdate = bsoup.find_all('span.date')[0].get_text()[:11]
    news_detail.append(pdate)

    _text = bsoup.find_all('div.par')[0].get_text().replace('\n', " ")
    btext = _text.replace("// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", "")
    news_detail.append(btext.strip())

    news_detail.append(n_url)

    return news_detail


def crawler(maxpage, query, s_date, e_date):
    s_from = s_date.replace(".", "")
    e_to = e_date.replace(".", "")
    page = 1
    maxpage_t = (int(maxpage) - 1) + 2
    f = open("C:/Ddump/contents_text.txt", 'w', encoding='utf-8')

    while page < maxpage_t:

        print(page)

        url = 'https://nsearch.chosun.com/search/total.search?query=' + query + '&siteid=www&category=21&field=paper&emd_word=%EB%8C%80%EC%9D%91&date_start=' + s_date + '&date_end=' + e_date + '&sort=0&pn=' + str(
            page)
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
        req = requests.get(url, headers=header)
        req.encoding = 'utf8'
        cont = req.text
        soup = BeautifulSoup(cont, 'html.parser')

        for urls in soup.select("dl.search_news > dt > a"):
            try:
                if urls["href"].startswith("http://nsearch.chosun.com/"):
                    news_detail = get_news(urls["href"])
                    f.write("{}\t{}\t{}\t{}\n".format(news_detail[1], news_detail[0], news_detail[2], news_detail[3]))
            except Exception as e:
                print(e)
                continue
        page += 1

    f.close()


def excel_make():
    data = pd.read_csv(RESULT_PATH + 'contents_text.txt', sep='\t', header=None, error_bad_lines=False)
    data.columns = ['years', 'title', 'contents', 'link']
    print(data)

    xlsx_outputFileName = '%s-%s-%s  %s시 %s분 %s초 result.xlsx' % (
    now.year, now.month, now.day, now.hour, now.minute, now.second)
    data.to_excel(RESULT_PATH + xlsx_outputFileName, encoding='utf-8')


def main():
    maxpage = input("최대 출력할 페이지수 입력하시오: ")
    query = input("검색어 입력: ")
    s_date = input("시작날짜 입력(20200101):")
    e_date = input("끝날짜 입력(20200101):")
    crawler(maxpage, query, s_date, e_date)

    excel_make()


main()