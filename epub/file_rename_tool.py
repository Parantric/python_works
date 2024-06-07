'''
一个处理 Z-Library 下载文件默认后缀名带有（Z-Library）的问题。
'''
import os.path
import re

SPLIT_WORDS = r'\s\(Z-Library\).*?\.'


def file_handle(file_path):
    """

    Args:
        file_path:

    Returns:

    """
    if os.path.isdir(file_path):
        files = os.listdir(file_path)
        for file in files:
            if len(re.findall(SPLIT_WORDS, file)) > 0:
                file_new = os.path.join(file_path, re.sub(SPLIT_WORDS, r'.', file))
                os.rename(os.path.join(file_path, file), file_new)
                print('=> 【' + file_new + '】')
    else:
        if len(re.findall(file_path, SPLIT_WORDS)) > 0:
            file_new = os.path.join(file_path, re.sub(SPLIT_WORDS, r'.', file_path))
            os.rename(file_path, file_new)
            print('=> 【' + file_new + '】')


if __name__ == '__main__':

    file_path = r'F:\backup_home\BaiduSyncdisk\books\pdf\数学基础'

    if os.path.exists(file_path):
        if '\\' in file_path:
            file_path = file_path.replace("\\", "/")
            file_handle(file_path)
            print('处理完成...')

    else:
        print('【' + file_path + '】' + ' 目录不存在！')
