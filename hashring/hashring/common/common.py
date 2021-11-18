# -*- coding: utf-8 -*-
from hashring.common.exceptions import ParameterError


def check_dev(dev):
    if type(dev['dev_id']) != int \
            or type(dev['dev_name']) != str \
            or type(dev['dev_weight']) != int \
            or type(dev['part_num']) != int:
        raise ParameterError
