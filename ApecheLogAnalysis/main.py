# -*- coding: utf-8 -*-
# Data : 2021/8/10 9:03 AM
from flask import Flask

from app.processing import DataAnalysis
from common import constant
app = Flask(__name__)


@app.route('/article_reports')
def article_reports():
    api = DataAnalysis()
    display_str = constant.ARTICLE_TITLE + constant.LINE_BREAK
    display_str += constant.ARTICLE_BREAK + constant.LINE_BREAK
    datas = api.article_reports()
    for data in datas:
        display_str += '| ' + ' | '.join(data) + ' |' + constant.LINE_BREAK
    return display_str


@app.route('/ip_reports')
def get_ip_reports():
    api = DataAnalysis()
    display_str = constant.IP_TITLE + constant.LINE_BREAK
    display_str += constant.IP_BREAK + constant.LINE_BREAK
    datas = api.ip_reports()
    for data in datas:
        display_str += '| ' + ' | '.join(data) + ' |' + constant.LINE_BREAK
    return display_str


@app.route('/complete_reports')
def get_complete_reports():
    api = DataAnalysis()
    display_str = constant.COMPLETE_TITLE + constant.LINE_BREAK
    display_str += constant.COMPLETE_BREAK + constant.LINE_BREAK
    datas = api.complete_reports()
    for data in datas:
        display_str += '| ' + ' | '.join(data) + ' |' + constant.LINE_BREAK
    return display_str


if __name__ == '__main__':
    app.run()
