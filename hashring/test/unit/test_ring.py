# -*- coding: utf-8 -*-
import unittest
import mock

from hashring.app.ringbuilder import RingBuilder
from hashring.common import exceptions as exc

DATAMANAGER = hasring.app.datamanager
RINGBUILDER = hasring.app.ringbuilder
COMMON = hashring.common.common


class TestRingBase(unittest.TestCase):
    u"""测试基类."""

    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestRingData(unittest.TestCase):
    u"""ring测试类."""

    def setUp(self):
        mock.patch('logging.getLogger', return_value=None)

    def tearDown(self):
        pass

    @mock.patch('%s.check_dev', COMMON)
    def test_add_dev_success(self, mock_check_dev):
        """测试成功添加设备。"""
        # 构造参数
        dev = {'dev_id': 430, 'dev_name': 'dev430', 'dev_weight': 2, 'part_num': 1}

        # 打桩
        mock_check_dev.return_value = None

        # 调用测试函数
        res = RingBuilder().add_dev(dev)

        # 校验返回值
        self.assertEqual(mock_check_dev.call_count, 1)
        self.assertIsNone(res)

    @mock.patch('%s.DataManager.load', DATAMANAGER)
    @mock.patch('%s.check_dev', COMMON)
    def test_add_dev_error(self, mock_check_dev, mock_load_dev_info):
        """测试添加设备,dev_id已存在抛出异常。"""
        # 构造参数
        dev = {'dev_id': 1, 'dev_name': 'dev1', 'dev_weight': 1, 'part_num': 1}

        # 打桩
        mock_check_dev.return_value = None
        mock_load_dev_info.return_value = {'1': dev}

        # 校验返回值
        self.assertRaises(exc.DevIdExistError, RingBuilder().add_dev(dev))
        self.assertEqual(mock_load_dev_info.call_count, 1)

    @mock.patch('%s.check_dev', COMMON)
    def test_update_dev_change_dev_weight(self, mock_check_dev):
        """测试成功更新设备信息, dev_weight发生变化。"""
        # 构造参数
        dev_id = 1
        dev = {'dev_id': 1, 'dev_name': 'dev1', 'dev_weight': 2, 'part_num': 1}

        # 打桩
        mock_check_dev.return_value = None

        # 调用测试函数
        res = RingBuilder().update_dev(dev_id, dev)

        # 校验返回值
        self.assertEqual(mock_check_dev.call_count, 1)
        self.assertIsNone(res)

    @mock.patch('%s.RingBuilder.rebalance', RINGBUILDER)
    @mock.patch('%s.check_dev', COMMON)
    def test_update_dev_with_same_dev_weight(self, mock_check_dev, moch_rebalance):
        """测试成功更新设备信息, dev_weight不变。"""
        # 构造参数
        dev_id = 1
        dev = {'dev_id': 1, 'dev_name': 'dev1', 'dev_weight': 2, 'part_num': 1}

        # 打桩
        mock_check_dev.return_value = None
        moch_rebalance.return_value = None

        # 调用测试函数
        res = RingBuilder().update_dev(dev_id, dev)

        # 校验返回值
        self.assertEqual(mock_check_dev.call_count, 1)
        self.assertEqual(moch_rebalance.call_count, 0)
        self.assertIsNone(res)

    @mock.patch('%s.DataManager.save', DATAMANAGER)
    def test_remove_dev_success(self, mock_save_file):
        """测试成功删除设备。"""
        # 构造参数
        dev_id = 1

        # 打桩
        mock_save_file.return_value = None

        # 调用测试函数
        res = RingBuilder().remove_dev(dev_id)

        # 校验返回值
        self.assertEqual(mock_save_file.call_count, 2)
        self.assertIsNone(res)

    @mock.patch('hashlib.hexdigest')
    def test_hash_dev(self, mock_hashlib_hexdigest):
        """测试指定key哈希到的物理设备."""
        # 构造参数
        key = '1:1'

        # 打桩
        mock_hashlib_hexdigest.return_value = '999'

        # 调用测试函数
        res = RingBuilder().hash_dev(key)

        # 校验返回值
        self.assertIsNotNone(res)
        self.assertEqual(mock_hashlib_hexdigest.call_count, 1)


if __name__ == '__main__':
    unittest.main()
