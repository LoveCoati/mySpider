import os
import time
import requests


class DownloadHtml:
    def __init__(self):
        self.user_info_url = "http://music.163.com/user/home?id="
        self.get_follows_url = "http://music.163.com/weapi/user/getfollows/"
        self.follows_data = "params=Ei5F4QJ9BIquMUdmX1z2LRUW3sVLnVIzpkVYTC8fG2tdSDwTb6P5kFsmk5Pa6m%2BfXzyHqAQk3%2Ff0RVwUoJ5rNbnyWSa%2FttZ5gODXiSAjegpVldGdQDL53JxCuoCoGgKmBAjNVm0PSUMNlkDkMdWwYg%3D%3D&encSecKey=1b820a0cb79ee270a986a0745a531af0cd472b89ae00cf6f6706edd5d65841268cc2d1a4424a026af0156bc7d91bc0e5288ab6341c1ed2a5e68da6f4f53c3f5bb63b08a6ca87f5abad3734fb8284aa38260be29d0a9af416e9c5b6ffb7ec953d91d9a19de638692faa0742c80742168f9fe77d084741621c59fea6ada0a26709"

        self.url_info_heaqders = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Connection":"keep-alive",
        "Host":"music.163.com",
        "Referer":"http://music.163.com/",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
        }

        self.follows_headers={
        "Host": "music.163.com",
        "Proxy-Connection": "keep-alive",
        "Content-Length": "436",
        "Cache-Control": "max-age=0",
        "Origin":" http://music.163.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Referer": "http://music.163.com/user/follows?id=1",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cookie": "JSESSIONID-WYYY=54; _iuqxldmzr_=25; Province=020; City=0755; _ntes_nnid=97ee19b18b40c8b2,1478153565823; _ntes_nuid=95d8ed655488691457ee19b18b40c8b2; __utma=9465024.962921247.1478153209.1478153209.1478153209.1; __utmb=9465624.4.10.1478153209; __utmc=94650624; __utmz=9465024"
        }

    def get_user_info(self, user_id, proxy):
        try:
            print("*"*20, "get_user_info: user_id ", user_id)
            url = self.user_info_url + str(user_id)
            if proxy is None:
                response = requests.get(url = url, headers = self.url_info_heaqders)
            else:
                response = requests.get(url = url, headers = self.url_info_heaqders, proxies = proxy, timeout=10)
            if response.status_code != 200:
                print("status: ", response.status_code)
                return None
            print("data len: ", len(response.text))
            return response.text
        except Exception as error_info:
            print("get_user_info: ", error_info)
            return None

    def get_follows_info(self, user_id, proxy):
        try:
            url = self.get_follows_url + str(user_id) + "?csrf_token="
            if proxy is None:
                response = requests.post(url = url, data = self.follows_data, headers = self.follows_headers)
            else:
                response = requests.post(url = url, data = self.follows_data, headers = self.follows_headers, proxies = proxy, timeout=10)
            if response.status_code != 200:
                print("status: ", response.status_code)
                return None
            print("data len: ", len(response.text))
            return response.text
        except Exception as error_info:
            print("get_follows_info: ", error_info)
            return None

    def get_fan_info(self, user_id, proxy):
        try:
            url = self.get_follows_url + str(user_id) + "?csrf_token="
            if proxy is None:
                response = requests.post(url = url, data = self.follows_data, headers = self.follows_headers)
            else:
                response = requests.post(url = url, data = self.follows_data, headers = self.follows_headers, proxies = proxy, timeout=10)
            if response.status_code != 200:
                print("status: ", response.status_code)
                return None
            print("data len: ", len(response.text))
            return response.text
        except Exception as error_info:
            print("get_fan_info: ", error_info)
            return None

    def test(self, user_id):
        self.get_user_info(user_id, None)
        self.get_follows_info(user_id, None)

if __name__ == "__main__":
    Test = DownloadHtml()
    Test.test(1)
    os.system("pause")

