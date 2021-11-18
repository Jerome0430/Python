# -*- coding: utf-8 -*-
# Data : 2021/8/9 3:03 PM

class LogFilteredNotExist(Exception):
    def __str__(self):
        return "待分析的日志数为零，请确认后重试！"
