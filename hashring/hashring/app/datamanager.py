# -*- coding: utf-8 -*-
import json
import os
import logging

LOG = logging.getLogger(__name__)


class DataManager(object):
    """Data manager."""

    @classmethod
    def load(cls, filename):
        u"""加载文件.

        :param filename: 文件名
        """
        try:
            with open(trans_filename(filename), 'r') as res_file:
                return json.load(res_file)
        except IOError:
            LOG.error('File(%s) is not exist, return {}', filename)
            return {}

    @classmethod
    def save(cls, filename, save_dict):
        u"""保存文件.

        :param filename: 文件名
        """
        with open(trans_filename(filename), 'w') as res_file:
            json.dump(save_dict, res_file)


def trans_filename(filename):
    """文件名转化为绝对路径"""
    return os.sep.join((os.getcwd(), filename))
