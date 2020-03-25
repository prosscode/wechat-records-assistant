# -*- coding: utf-8 -*-
# author:pross

import hashlib
import time

import xmltodict
from flask import Flask, make_response, request

app = Flask(__name__)
app.debug = True


@app.route('/')  # 默认网址
def index():
    return 'Index Page'


@app.route('/robot', methods=['GET', 'POST'])
def wechat_auth():  # 处理微信请求的处理函数，get方法用于认证，post方法取得微信转发的数据
    if request.method == 'GET':
        data = request.args
        if len(data) == 0:
            return "hello, this is handle view"
        token = 'mywechat'
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        # print(signature, timestamp, nonce, echostr)
        list = [token, timestamp, nonce]
        list.sort()
        temp = ''.join(list)
        sha1 = hashlib.sha1(temp.encode('utf-8'))
        hashcode = sha1.hexdigest()
        # print(hashcode)
        if hashcode == signature:
            return make_response(echostr)
        else:
            return ""
    else:  # 接收消息
        xml_data = request.stream.read()
        #解析数据
        dict_data = xmltodict.parse(xml_data)
        msg_type = dict_data['xml']['MsgType']
        print(xml_data)
        print(msg_type)
        # dispatchers = handle.MsgDispatcher(xml_data)
        # data = dispatchers.dispatch()
        if msg_type == 'text':
            content = dict_data['xml']['Conten']
            resp_xml ={
                'xml': {
                    'ToUserName': dict_data['xml']['FromUserName'],
                    'FromUserName': dict_data['xml']['ToUserName'],
                    'CreateTime': int(time.time()),
                    'MsgType': 'text',
                    'Content': content,
                }
            }
        response_msg = xmltodict.unparse(resp_xml)
        print(response_msg)

        # with open("./debug.log", "a") as file:
        #     file.write(data)
        #     file.close()
        # response = make_response(data)
        # response.content_type = 'application/xml'

        return response_msg


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8088)


