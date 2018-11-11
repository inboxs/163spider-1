import config
from utils import str_to_dict
from proxy import get_proxy
import _encrypt
import requests
import logging
import json
import sys
import re
from scrapy.selector import Selector
from pyquery import PyQuery as pq
sys.setrecursionlimit(1000000000)

# logging.basicConfig(level=logging.WARNING,
#                     format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

class Music:

    def __init__(self):
        self.headers = str_to_dict(config.HEADERS)
        self.url_mp3 = "https://music.163.com/weapi/song/enhance/player/url?csrf_token="
        self.url_comments = "https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?crsf_token="
        self.url_lyric = "https://music.163.com/weapi/song/lyric?csrf_token="
        self.url_detail = 'http://music.163.com/api/song/detail?ids=[{}]'

        self.params_mp3 = '{"ids":"[%s]","br":128000,"csrf_token":""}'
        self.params_comments = '{"rid":"R_SO_4_%s","offset":"%s","total":"true","limit":"%s","csrf_token":""}'
        self.params_lyric = '{"id":"%s","lv":-1,"tv":-1,"csrf_token":""}'


        self.song = "https://music.163.com/#/song?id={}"

        self.request = requests.Session()



    def proxy(self):
        ip = get_proxy()
        proxies = {
            'http': ip,
            'https': ip,
        }
        return proxies

    def get_encSEckey(self):
        encSEckey = _encrypt.get_encSecKey()
        return encSEckey

    # def get_comments_url(self,id):
    #      return "https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?crsf_token=".format(id)
    #
    # def get_params_mp3(self,id):
    #     return '{"ids":"[%s]","br":128000,"csrf_token":""}' % (id)
    #
    # def get_params_comments(self,id):
    #     return '{"rid":"R_SO_4_%s","offset":"%s","total":"true","limit":"%s","csrf_token":""}' % (id,id,id)


    def get_song_params(self,id,musicType):

        if musicType is "mp3":
            self.get_song_mp3(id,musicType)
        elif musicType is "comments":
            self.get_song_comments(id,musicType)
        elif musicType is "lyric":
            self.get_song_lysic(id,musicType)
        else:
            logging.info(msg="没有此类型")
            id = None

    # 歌曲
    def get_song_mp3(self,id,musicType):
        url_mp3 = self.url_mp3
        mp3 = self.params_mp3 % (id)
        self.parse_song(mp3, url_mp3, musicType,id)

    # 歌曲评论
    def get_song_comments(self,id,musicType,offset=0,limit=20):
        comments = self.params_comments % (id, offset, limit)
        url_comments = self.url_comments.format(id)
        self.parse_song(comments, url_comments, musicType,id)

    # 歌词
    def get_song_lysic(self,id,musicType):
        url_lyric = self.url_lyric
        lyric = self.params_lyric % (id)
        # logging.info(url_lyric)
        # logging.info(lyric)
        self.parse_song(lyric,url_lyric,musicType,id)

    # 解析json数据
    def parse_song(self,param,url,musicType,id):
        logging.info(url)
        logging.info(param)
        params = _encrypt.get_params(page=1, param=param)
        encSEckey = _encrypt.get_encSecKey()
        form_data = {
            "params": params,
            "encSecKey": encSEckey,
        }
        try:
            r = requests.post(url=url, headers=self.headers, data=form_data)
            content = r.text
            content = json.loads(content)
            data = self.parse_detail(id)
            if musicType == "mp3":
                if str(content["data"][0]["code"]) == str(200):
                    self.parse_mp3(content,data)
            elif musicType == "lyric":
                if not bool(content["sgc"]):
                    return
                if content:
                    self.parse_lyric(content,data)
                else:
                    print("没有")
            else:
                self.parse_comments(content,data, musicType)
        except:
            self.parse_song(param,url,musicType,id)

    # 解析歌曲
    def parse_mp3(self,content,data):
        c = content["data"][0]
        id = c["id"]
        url = c["url"]
        c = {
            "id":id,
            "url":url,
        }
        logging.info("歌曲名:{}-歌手名:{}".format(data["name"], data["singer"]))
        logging.info("获得歌曲地址:{}".format(c["url"]))

    # 解析歌曲信息
    def parse_detail(self,id):
        try:
            logging.info("解析歌曲id为{}的信息".format(id))
            r = requests.get(self.url_detail.format(id), headers=str_to_dict(config.HEADERS))
            content = r.text
            content = json.loads(content)
            if bool(content["songs"]):
                songs = content["songs"][0]
                name = songs["name"]
                artists = songs["artists"][0]
                singer = artists['name']
                data = {
                    "name": name,
                    "singer": singer,
                }
                logging.info("歌曲名:{}-歌手名:{}".format(data["name"], data["singer"]))
                return data
            else:
                logging.info("没有歌曲id为{}信息".format(id))
        except:
            self.parse_detail(id)


    # 解析评论
    def parse_comments(self,content,data,musicType):
        total = content["total"]
        if total >= 1:
            comments = content["comments"]
            # print(bool(content.get("hotComments")))
            logging.info("只获取部分评论")
            if bool(content.get("hotComments")):
                hotComments = content["hotComments"]
                logging.info("热评信息:")
                for hotComment in hotComments:
                    logging.info(hotComment)
                    logging.info("*"*50)
            for comment in comments:
                logging.info(comment)
                logging.info("*" * 50)

    # 解析歌词
    def parse_lyric(self,content,data):
        lyric = content["lrc"]["lyric"]
        nickname = ""
        try:
            nickname = content["lyricUser"]["nickname"]
        except:
            pass
        s = lyric
        lyric= ""
        count = 1
        for a in s.split('\n'):
            if a.strip(' '):
                g = re.sub(r'.*?]', "", a)
                lyric+=g+'\n'
        lyric_word = {
            "word":lyric,
            "nickname":nickname,
        }
        # logging.info("歌曲名:{}-歌手名:{}".format(data["name"],data["singer"]))
        logging.info("*"*30+"歌词"+"*"*30)
        logging.info(lyric_word["word"])
        logging.info("*" * 30 + "歌词" + "*" * 30)

# Music().get_song_params(id=36025590, musicType="mp3")