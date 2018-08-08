#!/bin/env python
# -*- coding:utf-8 -*-
# _auth:kaliarch

# 定义微信公众号信息
[common]
# 企业微信企业ID
corpid = wxe23xxxxxxxxxxx


# 接收消息服务器配置
[recmsg]

Token = mVNAAw3xxxxxxxxxxxxxxxxx
EncodingAESKey = vwbKImxc3WPeE073xxxxxxxxxxxxxxxxxx


# 自建应用信息
[appconfig]
# 自建应用agentid
agentid = 1000002
# 自建应用secret
secret = 6HAGX7Muw36pv5anxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 消息接收信息
# 消息接收用户id,如果多个用户用英文','隔开
userid = xuel|yaoy

# 消息接收部门id，如果多个用英文','隔开
partid = 11


[urlconfig]
# 获取应用token的api接口
get_access_token_url = https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}
# 发送消息api接口
send_msg_url = https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}
# 上传媒体api接口,获取mediaid
upload_media_url = https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={}&type=image
# 上传高清语音接口
upload_video_url = https://qyapi.weixin.qq.com/cgi-bin/media/get/jssdk?access_token={}&media_id={}

[loginfo]
#日志目录
logdir_name = logdir
#日志文件名称
logfile_name = wechat_server.log
