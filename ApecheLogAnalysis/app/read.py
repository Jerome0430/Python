# -*- coding: utf-8 -*-
# Data : 2021/8/9 3:03 PM
import os
import logging

LOG = logging.getLogger(__name__)
ILLEGAL_TYPES = ["js", "css", "*"]


class DataManager(object):
    """数据读取及简单的处理方法"""

    @classmethod
    def read_log(cls, filename):
        try:
            with open(trans_filename(filename)) as f:
                return f.readlines()

        except IOError:
            LOG.error('File (%s) is not exist, return []', filename)
            return []

    @classmethod
    def log_filter(cls, raw_logs):
        """
        对读取的原生log进行处理
        1. 删除错误数据格式
        2. 过滤后缀为js/css的记录
        3. 将数据整合为[ip, method, url, status_code]这样的格式
        :return: 形如[ip, method, url, status_code]的日志列表
        """
        log_lists = []
        for log in raw_logs:
            log_list = log.split(' ')
            if len(log_list) < 10:
                # 过滤错误格式的原始日志
                continue
            url = log_list[6]
            if not is_legal_type(url):
                continue
            ip, method, status = log_list[0], log_list[5], log_list[8]
            log_lists.append([ip, method, url, status])
        return log_lists


def is_legal_type(url):
    if url.endswith('js') or url.endswith('css'):
        return False
    return True


def trans_filename(filename):
    """文件名转化为绝对路径"""
    return os.sep.join((os.getcwd(), filename))
