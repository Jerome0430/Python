# -*- coding: utf-8 -*-

from __future__ import print_function
from sys import argv as sys_argv, exit
from hashring.app.ringbuilder import RingBuilder

EXIT_SUCCESS = 0
EXIT_ERROR = 2


class Commands(object):
    u"""命令行."""

    @staticmethod
    def add(dev):
        u"""添加设备."""
        return RingBuilder().add_dev(dev)

    @staticmethod
    def update(dev_id, dev):
        u"""更新设备.

        :param dev_id: 设备ID
        :param dev: 设备信息
        """
        return RingBuilder().update_dev(dev_id, dev)

    @staticmethod
    def remove(dev_id):
        u"""删除设备."""
        return RingBuilder().remove_dev(dev_id)

    @staticmethod
    def rebalance(dev_id, dev_weight, dict_ring_relationship):
        u"""重新平衡."""
        return RingBuilder().rebalance(dev_id, dev_weight, dict_ring_relationship)

    @staticmethod
    def hash_dev(key):
        u"""获取指定key hash到的设备."""
        return RingBuilder().hash_dev(key)


def main(arguments=None):
    global argv
    if arguments is not None:
        argv = arguments
    else:
        argv = sys_argv

    if len(argv) < 2:
        print("Invalid argument number.")
        exit(EXIT_ERROR)

    func = getattr(Commands, argv[1], None)
    if not func:
        print("Invalid argument.")
        exit(EXIT_ERROR)

    func()
    exit(EXIT_SUCCESS)
