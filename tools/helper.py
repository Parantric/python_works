# -*- coding:utf-8 -*-

def replace_path(old):
    '''
    转换 windows 环境下的路径分隔符
    Args:
        old:window 环境下的路径

    Returns:转换后的路径

    '''
    return old.replace('\\', '/')
