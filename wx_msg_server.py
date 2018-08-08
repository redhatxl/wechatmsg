#!/bin/env python
# -*- coding:utf-8 -*-
# _auth:kaliarch

from flask import Flask,request
from WXBizMsgCrypt import WXBizMsgCrypt
import xml.etree.cElementTree as ET
import sys
import time
import requests
import json
from configparser import ConfigParser
import logger


class WeChatMsg():
    def __init__(self,logger,host='0.0.0.0',port=8080):

        config = ConfigParser()
        config.read('config.py', encoding='utf-8')
        # 定义服务器监听地址和端口
        self.host = host
        self.port = port
        #
        self.sToken = config['recmsg']['Token']
        self.sEncodingAESKey = config['recmsg']['EncodingAESKey']
        self.sCorpID = config['common']['corpid']

        # 转发接收消息的应用信息配置
        self.agent_id = config['appconfig']['agentid']
        self.agent_secret = config['appconfig']['secret']
        self.userid = config['appconfig']['userid']
        self.partid = config['appconfig']['partid']
        self.send_msg_url = config['urlconfig']['send_msg_url']
        self.get_access_token_url = config['urlconfig']['get_access_token_url']

        # 服务器日志信息配置
        logger = logger.LogHelper()
        logname = logger.create_dir()
        self.logoper = logger.create_logger(logname)

        # 获取access_token
        self.access_token = json.loads(requests.get(self.get_access_token_url.format(self.sCorpID,self.agent_secret)).content)['access_token']

    def _send_text_msg(self, content):
        data = {
            "touser": ('|').join(self.userid.split(',')),
            "toparty": ('|').join(self.partid.split(',')),
            # "toparty":int(self.partid),
            "msgtype": "text",
            "agentid": self.agent_id,
            "text": {
                "content": content
            },
            "safe": 0
        }
        try:
            response = requests.post(self.send_msg_url.format(self.access_token), json.dumps(data))
            self.logoper.info(response.text)
            print(response.text)
            result_msg = json.loads(response.content)['errmsg']
            return result_msg
        except Exception as e:
            self.logoper.info(e)



    def _send_img_msg(self,mediaid):
        data = {
            "touser": ('|').join(self.userid.split(',')),
            "toparty": ('|').join(self.partid.split(',')),
            "msgtype": "image",
            "agentid": self.agent_id,
            "image": {
                "media_id": mediaid
            },
            "safe": 0
        }
        try:
            response = requests.post(self.send_msg_url.format(self.access_token), json.dumps(data))
            self.logoper.info(response.text)
            print response.text
            errmsg = json.loads(response.content)['errmsg']
            return errmsg
        except Exception as e:
            self.logoper.info(e)

    def _send_voice_msg(self,mediaid):
        data = {
            "touser": ('|').join(self.userid.split(',')),
            "toparty": ('|').join(self.partid.split(',')),
            "msgtype": "voice",
            "agentid": self.agent_id,
            "voice": {
                "media_id": mediaid
            },
        }
        try:
            response = requests.post(self.send_msg_url.format(self.access_token), json.dumps(data))
            self.logoper.info(response.text)
            print(response.text)
            result_msg = json.loads(response.content)['errmsg']
            return result_msg
        except Exception as e:
            self.logoper.info(e)

    def server_run(self):
        app = Flask(__name__)
        @app.route('/index', methods=['GET', 'POST'])
        def index():

            wxcpt = WXBizMsgCrypt(self.sToken, self.sEncodingAESKey, self.sCorpID)
            # 获取url验证时微信发送的相关参数
            sVerifyMsgSig = request.args.get('msg_signature')
            sVerifyTimeStamp = request.args.get('timestamp')
            sVerifyNonce = request.args.get('nonce')
            sVerifyEchoStr = request.args.get('echostr')

            # 验证url
            if request.method == 'GET':
                ret, sEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr)
                print type(ret)
                print type(sEchoStr)

                if (ret != 0):
                    print "ERR: VerifyURL ret:" + str(ret)
                    sys.exit(1)
                return sEchoStr

            # 接收客户端消息
            if request.method == 'POST':
                sReqMsgSig = sVerifyMsgSig
                sReqTimeStamp = sVerifyTimeStamp
                sReqNonce = sVerifyNonce
                sReqData = request.data
                print(sReqData)

                ret, sMsg = wxcpt.DecryptMsg(sReqData, sReqMsgSig, sReqTimeStamp, sReqNonce)
                print ret, sMsg
                if (ret != 0):
                    print "ERR: DecryptMsg ret: " + str(ret)
                    sys.exit(1)
                # 解析发送的内容并打印

                xml_tree = ET.fromstring(sMsg)
                print('xml_tree is ', xml_tree)

                # 被动的相应消息给客户端
                access_token = json.loads(requests.get(self.get_access_token_url.format(self.sCorpID, self.agent_secret)).content)['access_token']
                print(access_token)
                # access_token = 'GnSWpcQfG-6aDUQ83rmGeVeqXeQxueV9nYCPy2CSbaYwZcnZ2sh42PGkXardRbCjh-ZKsdMlcjPdSWETiYwjn_rQ-ttifkVj2lqnW1TsHAPsBuA-Rh2fM_eadcSDsKiJLphOaNvmscF6Sw9m6Fl-2Pv8dUCMrTWOE2WDTrAaZ4Bk6ab8RBYVzZL_rjxZziB2CiS3ujL0Gdoffowb9jh_HA'

                content_type = xml_tree.find("MsgType").text
                if content_type == "text":
                    content = xml_tree.find("Content").text
                    result = self._send_text_msg(content)
                    return result

                elif content_type == "image":
                    mediaid = xml_tree.find("MediaId").text
                    result = self._send_img_msg(mediaid)
                    return result
                elif content_type == "voice":
                    mediaid = xml_tree.find("MediaId").text
                    result = self._send_voice_msg(mediaid)
                    return result
                else:
                    content = None
                    return


        app.run(host=self.host, port=self.port, debug=True)


if __name__ == '__main__':
    wechatserver = WeChatMsg(logger)
    wechatserver.server_run()