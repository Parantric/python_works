# -*- coding:utf-8 -*-
import os.path
import subprocess as sp

if __name__ == '__main__':
    # 需要转码的 mkv 视频文件路径
    input_path = r'E:\temp_transfer\ali_cloudy\CloudDrive\阿里云盘Open\动漫珍藏\H海贼王\S002'
    # 如果是目录，则遍历文件
    if os.path.isdir(input_path):
        media_list = os.listdir(input_path)
        for medie_file in media_list:
            print(medie_file)
            input_file = os.path.join(input_path, medie_file)

            file_name, ext = os.path.splitext(medie_file)
            output_file = os.path.join(input_path, file_name + r'.mp4')

            sp.call((r'ffmpeg -i ' + input_file + ' -c:v copy -c:a aac ' + output_file),
                    shell=True)
