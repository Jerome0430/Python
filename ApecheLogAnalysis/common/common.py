# -*- coding: utf-8 -*-
# Data : 2021/8/9 3:03 PM
import json
import requests
import logging

LOG = logging.getLogger(__name__)


def get_title(url):
    """
    根据url获取文章标题
    :param url:
    :return: str
    """
    # 如果是页面文件，给出页面的标题，其它文件给出文件名
    if url.endswith('html') or url.endswith('htm'):
        try:
            response_text = requests.get(url).text
            return json.loads(response_text)['title']
        # 访问失败返回默认值
        except:
            return 'default title'
    return url.split('/')[-1].split('.')[0]
