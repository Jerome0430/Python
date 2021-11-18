# -*- coding: utf-8 -*-
import hashlib
import logging

from hashring.common import exceptions as exc
from hashring.common.common import check_dev
from hashring.app.datamanager import DataManager

LOG = logging.getLogger(__name__)


class RingBuilder(object):
    """ring builder."""

    def add_dev(self, dev):
        u"""添加设备.

        :param dev: 待添加的设备信息
        """
        LOG.info('Start to add dev: %s', dev)
        # 检验参数是否合法
        check_dev(dev)

        # 检查dev_id是否存在
        dict_dev_info = DataManager.load('dev_info.json')
        if dev['dev_id'] in dict_dev_info:
            LOG.error('Dev_id(%s) is already exist', dev['dev_id'])
            raise exc.DevIdExistError

        # 保存设备信息至文件
        dict_dev_info[dev['dev_id']] = dev
        DataManager.save('dev_info.json', dict_dev_info)

        # 重平衡
        dict_ring_relationship = DataManager.load('ring_relationship.json')
        self.rebalance(dev['dev_id'], dev['dev_weight'],
                       dict_ring_relationship=dict_ring_relationship)

    def update_dev(self, dev_id, dev):
        u"""更新设备信息.

        :param dev_id: 设备ID
        :param dev: 设备信息
        """
        LOG.info('Start to update dev_id(%s) to dev: %s', dev_id, dev)
        # 检验参数是否合法
        check_dev(dev)

        # 获取设备原有信息
        dict_dev_info = DataManager.load('dev_info.json')
        if dev_id in dict_dev_info:
            old_dev = dict_dev_info['dev_id']
        else:
            raise exc.DevIdNotExistError

        # 保存设备信息至文件
        dict_dev_info[dev['dev_id']] = dev
        DataManager.save('dev_info.json', dict_dev_info)

        # 如果权重改变，需要重平衡ring
        if old_dev['dev_weight'] != dev['dev_weight']:
            # 删除之前的映射关系
            dict_ring_relationship = DataManager.load('ring_relationship.json')
            for i in xrange(old_dev['dev_weight']):
                key = '%s:%s' % (dev_id, i)
                dev_hash = self.get_hash(key)
                dict_ring_relationship.pop(dev_hash)

            # 添加新的映射关系
            self.rebalance(dev_id, dev_weight=dev['dev_weight'],
                           dict_ring_relationship=dict_ring_relationship)

    def remove_dev(self, dev_id):
        u"""删除设备.

        :param dev_id: 待删除的设备ID
        """
        LOG.info('Start to remove dev, dev_id(%s)', dev_id)
        # 获取设备原有信息
        dict_dev_info = DataManager.load('dev_info.json')
        if dev_id in dict_dev_info:
            old_dev = dict_dev_info['dev_id']
        else:
            raise exc.DevIdNotExistError

        # 删除设备信息并保存
        dict_dev_info.pop(dev_id)
        DataManager.save('dev_info.json', dict_dev_info)

        # 删除映射关系并保存
        dict_ring_relationship = DataManager.load('ring_relationship.json')
        for i in xrange(old_dev['dev_weight']):
            key = '%s:%s' % (dev_id, i)
            dev_hash = self.get_hash(key)
            dict_ring_relationship.pop(dev_hash)
        DataManager.save('ring_relationship.json', dict_ring_relationship)

    def rebalance(self, dev_id, dev_weight, dict_ring_relationship):
        u"""重新平衡ring."""
        # 添加映射关系
        for i in xrange(dev_weight):
            key = '%s:%s' % (dev_id, i)
            dev_hash = self.get_hash(key)
            dict_ring_relationship[dev_hash] = dev_id

        # 保存映射关系
        DataManager.save('ring_relationship.json', dict_ring_relationship)

    def get_hash(self, key):
        u"""获取指定key的哈希值"""
        md5_str = hashlib.md5(key).hexdigest()
        return long(md5_str, 16)

    def hash_dev(self, key):
        u"""获取指定key hash到的设备.

        :param key: 指定key
        :return dev: 设备信息
        """
        # 获取key的hash值
        key_hash = self.get_hash(key)

        # 获取所有虚拟地址并排序
        list_ring_hash = []
        dict_ring_relationship = DataManager.load('ring_relationship.json')
        for keys in dict_ring_relationship:
            list_ring_hash.append(keys)
        list_ring_hash.sort()

        # 返回key应储存在的物理设备信息
        dict_dev_info = DataManager.load('dev_info.json')
        for hash_ring in list_ring_hash:
            if key_hash <= int(hash_ring):
                return dict_dev_info[str(dict_ring_relationship[hash_ring])]

        # 若循环一周未找到大于key的hash值的虚拟地址，返回最前面的虚拟地址对应的物理地址信息
        return dict_dev_info[str(dict_ring_relationship[list_ring_hash[0]])]
