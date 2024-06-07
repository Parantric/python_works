# -*- coding:utf-8 -*-
import json
import os

from _decimal import Decimal
from pymediainfo import MediaInfo

DEFAULT_FILE_EXT = ['.mp4', '.MP4', '.mkv', '.MKV', '.avi', '.AVI', ]


def get_files_item(file_dir: str, file_ext=DEFAULT_FILE_EXT):
    files_list = []
    if '\\' in file_dir:
        file_dir = file_dir.replace('\\', '/')
    if os.path.exists(file_dir):
        if os.path.isdir(file_dir):
            for file_path, dir_names, file_names in os.walk(file_dir):
                for file_name in file_names:
                    file_extension = os.path.splitext(file_name)[-1]
                    if file_extension in file_ext:
                        files_list.append(os.path.join(file_path, file_name))
        else:
            files_list.append(file_dir)

    else:
        print('【' + file_dir + '】' + '路径不存在...')
    return files_list


def get_mediainfo(file_list: list):
    print('---------------------------------------------------------------------')
    for file in file_list:
        file_path_item = os.path.split(file)
        print(file_path_item[-1])
        json_data = json.loads(MediaInfo.parse(file).to_json())
        for file_obj in json_data['tracks']:
            track_type = file_obj['track_type']
            if 'Video' == track_type:
                print('编码格式:',
                      file_obj['internet_media_type'] + r' ' + file_obj['commercial_name'] + r' (' + file_obj[
                          'format_info'] + r')')
                print('分辨率:', str(file_obj['width']) + r' x ' + str(file_obj['height']))
                frame_rate_mode = file_obj['frame_rate_mode']
                if 'CFR' == frame_rate_mode:
                    print('帧率模式:','CFR (恒定帧率)')
                elif 'VFR' == frame_rate_mode:
                    print('帧率模式:', 'VFR (可变帧率)')
                print('帧率:', file_obj['other_frame_rate'][0])
                bit_rate = file_obj['bit_rate']
                print('\n数据速率(Kbps):', str(Decimal(int(bit_rate) / 1000).quantize(Decimal("0"))))
                print('数据速率(Mbps):', str(Decimal(int(bit_rate) / 1000 / 1000).quantize(Decimal("0.00"))),'\n')
            elif 'Audio' == track_type:
                channel_s = file_obj['channel_s']
                if 2 == channel_s:
                    print('混音模式:', 'Stereo (立体声)')
                else:
                    print('混音模式:', '其它')
                print('音频格式:', file_obj['commercial_name'] + r' (' + file_obj['format_info'] + r')')
                print('音频采样率:', file_obj['other_sampling_rate'][0])
                print('音频比特率:', file_obj['other_bit_rate'][0])
        print('---------------------------------------------------------------------')
