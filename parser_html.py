import os
import json
from bs4 import BeautifulSoup

class ParserHtml:
    def __init__(self):
        pass

    def parser_user_info(self, data):
        try:
            user_info = {}
            soup = BeautifulSoup(data, "html.parser")
            t_name = soup.find("title").get_text()
            print(t_name)
            if " - " in t_name:
                user_info["nickname"] = t_name.split(' - ')[0]
            else:
                user_info["nickname"] = t_name
                if t_name == "网易云音乐":
                    return None
            user_info["area"] = soup.find("div", class_ = "inf s-fc3").find("span").get_text().split("：")[1]
            user_info["id"] = soup.find("div", id="m-record")["data-uid"]
            user_info["listen_nums"] = soup.find("div", id="m-record")["data-songs"]
            user_info["fan_count"] = soup.find("strong", id="fan_count").get_text()
            user_info["follow_count"] = soup.find("strong", id="follow_count").get_text()
            return user_info

        except Exception as error_info:
            print("parser_user_info: ", error_info)
            return None

    def parser_follows_info(self, data):
        try:
            follow_data = json.loads(data)
            return follow_data
        except Exception as error_info:
            print("parser_follows_info: ", error_info)
            return None

    def test(self):
        try:
            user_ifno = {}
            with open("test.html", "r", encoding= 'utf-8') as file:
                data = file.read()
            user_info = self.parser_user_info(data)
            print(user_info)

        except Exception as error_info:
            print("test: ", error_info)




if __name__ == "__main__":
    Test = ParserHtml()
    Test.test()
    os.system("pause")