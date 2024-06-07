# -*- coding:utf-8 -*-
from pymediainfo import MediaInfo
if __name__ == '__main__':
    file_path = r'E:\temp_transfer\ali_cloudy\阿里云盘Open\=================\绝世武魂\377.mkv'
    info = MediaInfo.parse(file_path)
    print(info.to_json())