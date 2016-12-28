import os
import re
import time
import random
import requests
import threading
from bs4 import BeautifulSoup


class IpProxy:

    def __init__(self):
        self.quit = False
        self.pages = 20
        self.thread_num = 200
        self.proxy_list = []
        self.proxy_use_list = []
        self.refresh_time = 600
        self.proxy_lock = threading.Lock()
        self.proxy_use_lock = threading.Lock()
        self.url = "http://www.xicidaili.com/nn/"
        self.file_url ="http://api.xicidaili.com/free2016.txt"
        self.test_url = "http://music.163.com/"
        self.headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Connection":"keep-alive",
        "Cookie":r"_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWM5NzY5ODhlZTFkYzU5ZmY5NzYzMWRiNzgwNDMzZGUxBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWFiMDdJYTl6S3pxVXNON1VZWWdtR21Gc09ZaDJGK2pVQytHNWNmR01NZms9BjsARg%3D%3D--8ebac226e1325680508a6da29df448cb78e2a427; CNZZDATA1256960793=1835877824-1478135294-%7C1478140742",
        "Host":"www.xicidaili.com",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
        }
        self.start_proxy()

    def get_proxy(self):
        if len(self.proxy_list) < 1:
            return None
        return self.proxy_list[random.randint(0, len(self.proxy_list) - 1)]

    def download_proxy(self):
        try:
            for page in range(1, self.pages):
                url = self.url + str(page)
                response = requests.get(url=url, headers=self.headers)
                if response.status_code != 200:
                    print("download_proxy error: ", url)
                    continue
                self.html_parser(response.text)
            response = requests.get(url=self.file_url, headers=self.headers)
            if response.status_code != 200:
                return

            for data in response.text.split('\r\n'):
                print(data)
                self.proxy_lock.acquire()
                self.proxy_list.append({"http": "http://" + data})
                self.proxy_lock.release()

            self.html_parser_2()

        except Exception as error_info:
            print("refresh_proxy: ", error_info)

    def refresh_proxy(self):
        while not self.quit:
            self.download_proxy()
            self.test_threads()
            print("refresh_proxy sleep ......")
            print("can use proxy number: ", len(self.proxy_use_list))
            time.sleep(self.refresh_time)

    def html_parser(self, data):
        try:
            soup = BeautifulSoup(data, "html.parser")
            trs = soup.find('table', id='ip_list').find_all('tr')
            for tr in trs[1:]:
                tds = tr.find_all('td')
                ip = tds[1].text.strip()
                port = tds[2].text.strip()
                protocol = tds[5].text.strip()
                if protocol == "HTTP" or protocol == "HTTPS":
                    # print ('%s=%s:%s' % (protocol, ip, port))
                    self.proxy_lock.acquire()
                    self.proxy_list.append({"http": r'http://%s:%s' % (ip, port)})
                    self.proxy_lock.release()
        except Exception as error_info:
            print("html_parser: ", error_info)
            return None

    def html_parser_2(self):
        for index in range(2, 6):
            headers = dict(self.headers)
            headers["Host"] = "http://www.youdaili.net"
            url = "http://www.youdaili.net/Daili/http/12644_" + str(index) + ".html"
            print(url)
            headers["Referer"] = url
            response = requests.get(url=url, headers=self.headers)
            if response.status_code != 200:
                print("error")
                continue
            else:
                f = re.compile(r'[\d]+.[\d]+.[\d]+.[\d]+:[\d]+')
                ip_list = f.findall(response.text)
                for ip in ip_list:
                    print("html_parser_2: ", ip)
                    self.proxy_lock.acquire()
                    self.proxy_list.append({"http": r"http://" + ip})
                    self.proxy_lock.release()


    def test_proxy(self, index):
        try:
            while len(self.proxy_list) > 0:
                self.proxy_lock.acquire()
                proxy = self.proxy_list.pop(0)
                self.proxy_lock.release()
                print("test_proxy: ", index, " test proxy: ", proxy)
                response = requests.get(url = self.test_url, headers=self.headers, proxies = proxy, timeout=5)
                if response.status_code != 200:
                    if proxy in self.proxy_use_list:
                        self.proxy_use_lock.acquire()
                        self.proxy_use_list.delete(proxy)
                        self.proxy_use_lock.release()
                    continue
                else:
                    if proxy not in self.proxy_use_list:
                        self.proxy_use_lock.acquire()
                        self.proxy_use_list.append(proxy)
                        self.proxy_use_lock.release()
        except Exception as error_info:
            print("test_proxy: ", error_info)

    def test_threads(self):
        threads = []
        for index in range(0, self.thread_num):
            th = threading.Thread(target = self.test_proxy, args=(index,))
            threads.append(th)

        for th in threads:
            th.start()

        # for th in threads:
        #     threading.Thread.join(th)

    def start_proxy(self):
        th = threading.Thread(target = self.refresh_proxy)
        th.start()

if __name__ == "__main__":
    Test = IpProxy()








