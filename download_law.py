import time
import requests
import json
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


def get_url_list():
    '''获取国税网所有增值税的政策文件url'''
    url = "http://www.chinatax.gov.cn/api/query?siteCode=bm29000fgk&tab=all&key=9A9C42392D397C5CA6C1BF07E2E0AA6F"
    ua = UserAgent()
    url_list = []

    for page in range(12, 76):
        headers = {"User-Agent": ua.random}
        data = {
            'timeOption': '0',
            'page': page.__str__(),
            'pageSize': '10',
            'keyPlace': '1',
            'qt': '增值税',
            'sort': 'dateDesc'
        }

        time.sleep(0.4)
        print('querying page {}'.format(page))
        respond = requests.post(url, data=data, headers=headers)

        for obj in json.loads(respond.text)['resultList']:
            url_list.append(obj['url'])

    with open('urls.txt', 'w', encoding='utf-8') as f:
        for url in url_list:
            f.write(url + '\n')


def get_text():
    '''根据url列表获取政策内容'''
    urls = []
    with open('urls.txt', 'r', encoding='utf-8') as f:
        urls = f.readlines()
    i = 1
    for url in urls:
        url = url.strip()
        ua = UserAgent()
        headers = {"User-Agent": ua.random}

        respond = requests.get(url, headers=headers)
        respond.encoding = 'utf-8'

        soup = BeautifulSoup(respond.text, 'html.parser')
        div = soup.find('div', class_='text', id='fontzoom')
        result = div.find_all('p', style="text-indent: 2em; text-align: justify;")
        if result.__len__() == 0:
            print('!!! Writing file No.{} but using origin text'.format(i))
            with open(i.__str__() + '_origin.txt', 'w', encoding='utf-8') as f:
                f.write(div.text)
        else:
            print('Writing file No.' + i.__str__())
            with open(i.__str__() + '.txt', 'w', encoding='utf-8') as f:
                for p in result:
                    if p.find('br'): break  # 从<br>开始是附件和日期等信息, 删除
                    f.write(p.text + '\n')

        time.sleep(1)
        i += 1


if __name__ == '__main__':
    # get_url_list()
    get_text()
    url = 'http://www.chinatax.gov.cn/chinatax/n359/c10859408/content.html'
    ua = UserAgent()
    headers = {"User-Agent": ua.random}

    respond = requests.get(url, headers=headers)
    respond.encoding = 'utf-8'

    soup = BeautifulSoup(respond.text, 'html.parser')
    print(soup.text)
