import MySQLdb
import download_html
import parser_html
import ip_proxy
import threading
import os
import json


class UrlManage:
    def __init__(self):
        self.user_id = 166038
        self.thread_num = 1000
        self.sql_lock = threading.Lock()
        self.user_list_lock = threading.Lock()
        self.user_id_lock = threading.Lock()
        self.download_html = download_html.DownloadHtml()                   # 下载器
        self.parser_html   = parser_html.ParserHtml()                     # 解释器
        # self.ip_proxy = ip_proxy.IpProxy()                             # ip代理
        # self.ip_proxy.quit = True
        self.config()

    def config(self):
        if not os.path.exists("config.txt"):
            print("没有读取到数据库配置文件")
            os.system("pause")
            os._exit(1)
        else:
            with open("config.txt", "r") as file:
                data = file.read()
            try:
                json_data = json.loads(data)
                self.user_name  = json_data["user_name"]
                self.db_name    = json_data["db_name"]
                self.db_passwd  = json_data["db_passwd"]
                self.db_ip_addr = json_data["db_ip_addr"]
                self.conn = MySQLdb.connect(host=self.db_ip_addr, user=self.user_name, passwd=self.db_passwd,
                                    db=self.db_name, charset="utf8")
                self.cursor = self.conn.cursor()
            except Exception as error_info:
                print(error_info)
                os.system("pause")
                os._exit(1)

    def exit_init(self):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()
        exit()

    def start(self):
        while self.user_id  < 2000000:
            self.user_id_lock.acquire()
            self.user_id += 1
            user_id = self.user_id
            self.user_id_lock.release()

            try:
                # proxy = self.ip_proxy.get_proxy()
                # print("get proxy: ", proxy)
                proxy = None                                                     # 不使用代理

                user_data = self.download_html.get_user_info(user_id, proxy)     # 获取用户的信息
                if user_data is None:
                    print("*"*20, "user_data is None ")
                    continue
                user_info = {}
                user_info = self.parser_html.parser_user_info(user_data)
                if user_info != None:
                    sql = "insert into t_user_info (f_user_id, f_songs, f_nick_name, f_follow_count, f_fan_count,f_area) value('%d', '%d', '%s', '%d', '%d', '%s')" % (int(user_info["id"]), int(user_info["listen_nums"]), user_info["nickname"], int(user_info["follow_count"]),int(user_info["fan_count"]), user_info["area"])
                    print(sql)
                    self.sql_lock.acquire()
                    self.cursor.execute(sql)
                    self.sql_lock.release()

                    follow_data = self.download_html.get_follows_info(user_id, proxy)   # 用户关注
                    if follow_data is None:
                        continue
                    follow_info ={}
                    follow_info = self.parser_html.parser_follows_info(follow_data)
                    if follow_info != None:
                        for follow_child_data in follow_info["follow"]:
                            sql = "insert into t_followed_info (f_parent_id, f_child_id) value('%d', '%d')" %  (int(user_info["id"]), int(follow_child_data["userId"]))
                            print(sql)
                            self.sql_lock.acquire()
                            self.cursor.execute(sql)
                            self.sql_lock.release()

            except Exception as error_info:
                print(error_info)
                self.user_id_lock.acquire()
                self.user_id_list.append(user_id)
                self.user_id_lock.release()



    def start_threads(self):
        threads = []
        for index in range(0, self.thread_num):
            th = threading.Thread(target=self.start)
            threads.append(th)

        for th in threads:
            th.start()

        for th in threads:
            threading.Thread.join(th)


if __name__ == "__main__":
    Test = UrlManage()
    Test.start_threads()





