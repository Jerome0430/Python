# -*- coding: utf-8 -*-
# Data : 2021/8/10 9:03 AM

import unittest

from app.read import DataManager


class TestRead(unittest.TestCase):
    """
    日志解析测试类
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_read_log(self):
        # 文件目录存在
        res = DataManager.read_log('test.log')
        self.assertIsNotNone(res)
        # 文件目录不存在
        res = DataManager.read_log('')
        self.assertEqual(res, [])

    def test_log_filter(self):
        raw_logs = ['200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/miniprj/material.html HTTP/1.1" 200 38093\n',
                    '200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plus/search.css HTTP/1.1" 200 1095\n']
        res = DataManager.log_filter(raw_logs)
        self.assertIsNotNone(res)


if __name__ == '__main__':
    unittest.main()
