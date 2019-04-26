# coding=utf-8

import json
import requests
import sys


RTX_WEBHOOK_URL = "http://in.qyapi.weixin.qq.com/cgi-bin/webhook/send?key=44d3070d-bb8a-47cd-a741-356b431638d4"


def push_to_rtx(msg_json):
    print('\r\nposting to rtx...')
    r = requests.post(RTX_WEBHOOK_URL, json=msg_json)
    print(r.text + "\r\n")
    print(r.status_code, r.reason, "\r\n\r\n")


def generate_rtx_markdown(text):
    data = {}
    data['msgtype'] = 'markdown'
    data['markdown'] = {}
    data['markdown']['content'] = str(text)
    print(data)
    return data

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        print('no args')
        sys.exit(-1)
    msg = args[0]
    print('pushing [',msg,'] to rtx...')
    push_to_rtx(generate_rtx_markdown(msg))