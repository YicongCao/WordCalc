# coding=utf-8
import os
import random
import json

import push

from flask import (Flask, request)
from wordcalc import WordCalc

log_to_bot = True
word_calc = WordCalc()


def parse_formular(formular_str):
    # 输入：马化腾-腾讯+阿里巴巴
    # 切分：pos: ['马化腾', '阿里巴巴'] neg: ['腾讯']
    f_str = str(formular_str).strip()
    # 简单滤除无关词
    f_str = f_str.replace("等于", "").replace("多少", "").replace("什么", "")
    if not f_str.endswith("+"):
        f_str = f_str + "+"
    pos = []
    neg = []
    item_start = -1
    isAdd = True
    for i in range(0, len(f_str)):
        # 先结算前头的
        if f_str[i] == "+" or f_str[i] == "-":
            # 滤除符号
            item = f_str[item_start + 1:i].strip()
            if '' != item:
                if isAdd:
                    pos.append(item)
                else:
                    neg.append(item)
            # 然后记录这次的符号
            item_start = i
            if f_str[i] == "+":
                isAdd = True
            elif f_str[i] == "-":
                isAdd = False
    return pos, neg


def create_app():
    app = Flask(__name__)

    # 处理单词计算请求
    @app.route('/wordcalc', methods=('GET', 'POST'))
    def do_word_calc():
        global word_calc, log_to_bot
        # GET 和 POST 都行
        if request.method == 'POST':
            post_body = str(request.data.decode('utf-8'))
        elif request.method == 'GET':
            post_body = str(request.args.get("q"))
        if "" == post_body:
            resp = {
                "ret": 0,
                "msgtype": "markdown",
                "text": "喵喵喵？",
                "pic": "nopic"
            }
            return json.dumps(resp, indent=4, ensure_ascii=False)
        # 解析提问句
        pos, neg = parse_formular(post_body)
        # 使用 gensim/annoy
        result = word_calc.calc(pos, neg)
        if log_to_bot:
            push.push_to_rtx(push.generate_rtx_markdown(
                post_body + "=\r\n" + str(result)))
        # 过滤掉重复词
        filtered_result = []
        for item in result:
            if item[0] not in pos and item[0] not in neg:
                filtered_result.append(item[0])
        # 生成文本回复
        resp_choices = []
        if len(filtered_result) == 0:
            resp_choices.append("臣妾实在算不出啊")
            resp_choices.append("算晕了，今天天气不错，用云计算试试？")
            resp_choices.append("程序已崩溃")
            resp_choices.append("爆炸倒计时: 3...2...1...")
        elif len(filtered_result) < 3:
            item = random.choice(filtered_result)
            resp_choices.append(item)
            resp_choices.append("也许等于" + item + "？")
            resp_choices.append("答案是" + item + "～")
        else:
            items = random.choices(filtered_result, k=3)
            resp_choices.append("大概也许是{0}、{1}或{2}".format(
                items[0], items[1], items[2]))
            resp_choices.append("等于{0}".format(items[0]))
            resp_choices.append("我算出来的结果是{0}".format(items[0]))
            resp_choices.append("大概也许是{0}".format(items[0]))
            resp_choices.append("答案是{0}、{1}或{2}".format(
                items[0], items[1], items[2]))
            resp_choices.append("你是想说{0}和{1}吗？".format(
                items[0], items[1]))
        # 按业务约定返回结果
        resp = {
            "ret": 0,
            "msgtype": "markdown",
            "text": random.choice(resp_choices),
            "pic": "nopic"
        }
        return json.dumps(resp, indent=4, ensure_ascii=False)

    # 处理开关日志推送请求
    @app.route('/switch', methods=('GET', 'POST'))
    def switch_log_to_bot():
        global log_to_bot
        log_to_bot = not log_to_bot
        if (log_to_bot):
            push.push_to_rtx(push.generate_rtx_markdown("bot调用日志已开启"))
        else:
            push.push_to_rtx(push.generate_rtx_markdown("bot调用日志已关闭"))
        return "succ"

    # 处理训练annoy有损匹配模型请求
    @app.route('/annoy', methods=('GET', 'POST'))
    def train_with_annoy():
        global word_calc
        push.push_to_rtx(push.generate_rtx_markdown("收到训练annoy请求"))
        word_calc.train_with_annoy()
        push.push_to_rtx(push.generate_rtx_markdown("annoy请求处理完毕"))
        return "succ"

    return app


if __name__ == "__main__":
    # 将数据导入 gensim
    word_calc.train_with_gensim()
    # 拉起 flask web 服务
    push.push_to_rtx(push.generate_rtx_markdown("flask初号机已就位"))
    create_app().run(host='0.0.0.0', port=5000)
