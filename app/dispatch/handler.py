# -*- coding: utf-8 -*-
# author:pross

import time
import xmltodict
from app.dispatch import robot


class MsgParser(object):
    """
       用于解析从公众平台传递过来的参数，并进行解析
    """

    def __init__(self, msg):
        self.data = msg['xml']
        print(self.data)

    def parse(self):
        # 消息id 64位整型
        self.msg_id = self.data['MsgId']
        # 发给谁
        self.master = self.data['ToUserName']
        # 谁发的
        self.user = self.data['FromUserName']
        # 发送时间
        self.create_time = self.data['CreateTime']
        # 消息媒体id，可以调用获取临时素材接口拉取数据
        self.media_id == self.data['MediaId']

        # 消息类型
        self.type = self.data['MsgType']
        if self.type == 'text':  # 文本消息
            self.content = self.data['Content']
        elif self.type == 'image':  # 图片消息
            self.pic_url = self.data['PicUrl']
        elif self.type == 'voice':  # 语音消息
            self.format = self.data['Format']
            self.recognition = self.data['Recognition']
        elif self.type == 'video' or self.type == 'shortvideo':  # 视频消息
            self.thumb_mediaId == self.data['ThumbMediaId']
        elif self.type == 'location':  # 地理位置消息
            self.location == self.data['location']
        elif self.type == 'link':  # 链接消息
            self.link == self.data['link']

        return self


class MsgDispatcher(object):
    """
       根据消息的类型，获取不同的处理返回值
    """

    def __init__(self, data):
        print("=======enter dispatcher=======")
        # 解析xml数据
        dict_data = xmltodict.parse(data)
        parser = MsgParser(dict_data).parse()
        self.msg = parser
        self.handler = MsgHandler(parser)

    def dispatch(self):
        self.result = ""  # 统一的公众号出口数据
        if self.msg.msgtype == "text":
            self.result = self.handler.textHandle()
        elif self.msg.msgtype == "voice":
            self.result = self.handler.voiceHandle()
        elif self.msg.msgtype == 'image':
            self.result = self.handler.imageHandle()
        elif self.msg.msgtype == 'video':
            self.result = self.handler.videoHandle()
        elif self.msg.msgtype == 'shortvideo':
            self.result = self.handler.shortVideoHandle()
        elif self.msg.msgtype == 'location':
            self.result = self.handler.locationHandle()
        elif self.msg.msgtype == 'link':
            self.result = self.handler.linkHandle()
        elif self.msg.msgtype == 'event':
            self.result = self.handler.eventHandle()

        return self.result


class MsgHandler(object):
    """
        针对type不同，转交给不同的处理函数。直接处理即可
    """

    def __init__(self, msg):
        self.msg = msg
        self.time = int(time.time())

        def textHandle(self, user='', master='', time='', content=''):
            template = """
                <xml>
                     <ToUserName><![CDATA[{}]]></ToUserName>
                     <FromUserName><![CDATA[{}]]></FromUserName>
                     <CreateTime>{}</CreateTime>
                     <MsgType><![CDATA[text]]></MsgType>
                     <Content><![CDATA[{}]]></Content>
                 </xml>
                """
            # 对用户发过来的数据进行解析，并执行不同的路径
            try:
                response = robot.get_response_by_keyword(self.msg.content)
                if response['type'] == "image":
                    result = self.imageHandle(self.msg.user, self.msg.master, self.time, response['content'])
                elif response['type'] == "music":
                    data = response['content']
                    result = self.musicHandle(data['title'], data['description'], data['url'], data['hqurl'])
                elif response['type'] == "news":
                    items = response['content']
                    result = self.newsHandle(items)
                # 这里还可以添加更多的拓展内容
                else:
                    response = robot.get_turing_response(self.msg.content)
                    result = template.format(self.msg.user, self.msg.master, self.time, response)
                # with open("./debug.log", 'a') as f:
                #   f.write(response['content'] + '~~' + result)
                #    f.close()
            except Exception as e:
                with open("./debug.log", 'a') as f:
                    f.write("text handler:" + str(e.message))
                    f.close()
            return result

        def musicHandle(self, title='', description='', url='', hqurl=''):
            template = """
                <xml>
                     <ToUserName><![CDATA[{}]]></ToUserName>
                     <FromUserName><![CDATA[{}]]></FromUserName>
                     <CreateTime>{}</CreateTime>
                     <MsgType><![CDATA[music]]></MsgType>
                     <Music>
                     <Title><![CDATA[{}]]></Title>
                     <Description><![CDATA[{}]]></Description>
                     <MusicUrl><![CDATA[{}]]></MusicUrl>
                     <HQMusicUrl><![CDATA[{}]]></HQMusicUrl>
                     </Music>
                     <FuncFlag>0</FuncFlag>
                </xml>
                """
            response = template.format(self.msg.user, self.msg.master, self.time, title, description, url, hqurl)
            return response

        def voiceHandle(self):
            response = robot.get_turing_response(self.msg.recognition)
            result = self.textHandle(self.msg.user, self.msg.master, self.time, response)
            return result

        def imageHandle(self, user='', master='', time='', mediaid=''):
            template = """
                <xml>
                     <ToUserName><![CDATA[{}]]></ToUserName>
                     <FromUserName><![CDATA[{}]]></FromUserName>
                     <CreateTime>{}</CreateTime>
                     <MsgType><![CDATA[image]]></MsgType>
                     <Image>
                     <MediaId><![CDATA[{}]]></MediaId>
                     </Image>
                 </xml>
                """
            if mediaid == '':
                response = self.msg.mediaid
            else:
                response = mediaid
            result = template.format(self.msg.user, self.msg.master, self.time, response)
            return result

        def videoHandle(self):
            return 'video'

        def shortVideoHandle(self):
            return 'shortvideo'

        def locationHandle(self):
            return 'location'

        def linkHandle(self):
            return 'link'

        def eventHandle(self):
            return 'event'

        def newsHandle(self, items):
            # 图文消息这块真的好多坑，尤其是<![CDATA[]]>中间不可以有空格，可怕极了
            articlestr = """
                <item>
                    <Title><![CDATA[{}]]></Title>
                    <Description><![CDATA[{}]]></Description>
                    <PicUrl><![CDATA[{}]]></PicUrl>
                    <Url><![CDATA[{}]]></Url>
                </item>
                """
            itemstr = ""
            for item in items:
                itemstr += str(articlestr.format(item['title'], item['description'], item['picurl'], item['url']))

            template = """
                <xml>
                    <ToUserName><![CDATA[{}]]></ToUserName>
                    <FromUserName><![CDATA[{}]]></FromUserName>
                    <CreateTime>{}</CreateTime>
                    <MsgType><![CDATA[news]]></MsgType>
                    <ArticleCount>{}</ArticleCount>
                    <Articles>{}</Articles>
                </xml>
                """
            result = template.format(self.msg.user, self.msg.master, self.time, len(items), itemstr)
            return result
