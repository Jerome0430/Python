# -*- coding: utf-8 -*-
# Data : 2021/8/9 3:03 PM
import logging
from collections import Counter

from app.read import DataManager
from common.common import get_title
from common import exceptions

LOG = logging.getLogger(__name__)


class DataAnalysis(object):

    def __init__(self):
        self.raw_logs = DataManager.read_log('apeche.log')
        self.log_lists = DataManager.log_filter(self.raw_logs)
        if not self.log_lists:
            raise exceptions.LogFilteredNotExist()

    def article_reports(self):
        """
        根据过滤得到的数据 处理得到文章报表
        输入 [[ip, method, url, status_code]]
        :return: [[url, title, count_visit, count_ips]]
        """
        article_reports = []
        url_set = set(log[2] for log in self.log_lists)
        for url in url_set:
            title = get_title(url)
            # 对于每一个url，要维护访问这个url的次数、访问它的ip列表
            ips = set()
            count = 0
            for log in self.log_lists:
                if url == log[2]:
                    count += 1
                    ips.add(log[0])
            article_reports.append([url, title, str(count), str(len(ips))])
        return article_reports

    def ip_reports(self):
        """
        将过滤后的数据处理为ip报表
        输入 [[ip, method, url, status_code]]
        :return: [[ip, count_visit, count_articles]]
        """
        ips = set([log[0] for log in self.log_lists])
        ip_reports = []
        for ip in ips:
            urls = set()
            count = 0
            for log in self.log_lists:
                if ip == log[0]:
                    count += 1
                    urls.add(log[2])
            ip_reports.append([ip, str(count), str(len(urls))])
        return ip_reports

    def complete_reports(self):
        """
        将过滤后的数据处理为完整的报表
        输入 [[ip, method, url, status_code]]
        :return: [[ip, url, count_visit]]
        """
        # 将log中的ip和url组合成键，进行计数
        complete_reports = []
        tmp = []
        for log in self.log_lists:
            tmp.append(' '.join([log[0], log[2]]))
        counter = Counter(tmp)
        for info in counter:
            count = counter.get(info)
            [ip, url] = info.split(' ')
            complete_reports.append([ip, url, str(count)])
        return complete_reports
