# -*- coding: utf-8 -*-
# Data : 2021/8/10 9:03 AM

import unittest
import random
import string
import mock

from app.processing import DataAnalysis
from common import exceptions


class TestProcessing(unittest.TestCase):
    """
    日志解析测试
    """

    def setUp(self):
        self.raw_logs = []
        # 构造100w条数据
        for i in range(1000000):
            ip = '200.%s.%s.%s' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            method = 'GET'
            status = '200'
            url = '/test_url/%s.%s' % (''.join(random.sample(string.ascii_letters + string.digits, 8)),
                                       random.choice(['html', 'htm', 'css', 'js', 'pdf']))
            self.raw_logs.append([ip, method, url, status])

    def tearDown(self):
        pass

    @mock.patch('app.read.DataManager.log_filter')
    @mock.patch('app.read.DataManager.read_log')
    def test_article_reports(self, mock_read_log, mock_log_filter):
        # 正常读取到日志数据

        # 构造数据
        api = DataAnalysis()

        # 打桩
        mock_read_log.return_value = self.raw_logs
        mock_log_filter.return_value = self.raw_logs

        # 调用测试函数
        res = api.article_reports()

        # 校验返回值
        self.assertIsNotNone(res)

        # 未读取到日志数据
        mock_log_filter.return_value = []
        with self.assertRaises(exceptions.LogFilteredNotExist):
            DataAnalysis()

    @mock.patch('app.read.DataManager.log_filter')
    @mock.patch('app.read.DataManager.read_log')
    def test_ip_reports(self, mock_read_log, mock_log_filter):
        # 正常读取到日志数据

        # 构造数据
        api = DataAnalysis()

        # 打桩
        mock_read_log.return_value = self.raw_logs
        mock_log_filter.return_value = self.raw_logs

        # 调用测试函数
        res = api.ip_reports()

        # 校验返回值
        self.assertIsNotNone(res)

        # 未读取到日志数据
        mock_log_filter.return_value = []
        with self.assertRaises(exceptions.LogFilteredNotExist):
            DataAnalysis()

    @mock.patch('app.read.DataManager.log_filter')
    @mock.patch('app.read.DataManager.read_log')
    def test_complete_reports(self, mock_read_log, mock_log_filter):
        # 正常读取到日志数据

        # 构造数据
        api = DataAnalysis()

        # 打桩
        mock_read_log.return_value = self.raw_logs
        mock_log_filter.return_value = self.raw_logs

        # 调用测试函数
        res = api.complete_reports()

        # 校验返回值
        self.assertIsNotNone(res)

        # 未读取到日志数据
        mock_log_filter.return_value = []
        with self.assertRaises(exceptions.LogFilteredNotExist):
            DataAnalysis()


if __name__ == '__main__':
    unittest.main()
