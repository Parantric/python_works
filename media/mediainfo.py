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


def get_mediainfo(data_list: list):
    print('---------------------------------------------------------------------')
    for data in data_list:
        #
        print(f"{data['file_name']}\n")
        print('编码格式:', data['v_code_name'])
        print('分辨率:', data['v_resolution'])
        print('帧率模式:', data['v_frame_rate_mode'])
        print(f"帧率:{data['v_frame_rate']}\n")
        print('数据速率(Kbps):', data['v_k_bit_rate'])
        print(f"数据速率(Mbps):{data['v_m_bit_rate']}\n")
        print('混音模式:', data['a_channel_type'])
        print('音频格式:', data['a_commercial_name'])
        print('音频采样率:', data['a_sampling_rate'])
        print('音频比特率:', data['a_bit_rate'])
        print('---------------------------------------------------------------------')


def mediainfo_handler(file_list: list):
    '''
    处理通过 MediaInfo 工具直接返回的数据，然后封装为对象.
    Args:
        file_list:视频文件列表

    Returns:包含封装好的视频信息对象的列表

    '''
    media_data_list = []
    for file in file_list:
        # 文件名
        media_data = {'file_name': os.path.split(file)[-1]}

        json_data = json.loads(MediaInfo.parse(file).to_json())
        for file_obj in json_data['tracks']:
            track_type = file_obj['track_type']
            # 视频信息
            if 'Video' == track_type:
                # 视频编码格式
                internet_media_type = file_obj['internet_media_type']
                if 'H265' in internet_media_type or 'h265' in internet_media_type:
                    internet_media_type = 'H.265'
                elif 'H264' in internet_media_type or 'H264' in internet_media_type:
                    internet_media_type = 'H.264'

                media_data['v_code_name'] = internet_media_type + r' ' + file_obj['commercial_name'] + r' (' + file_obj[
                    'format_info'] + r')'

                # 分辨率
                media_data['v_resolution'] = str(file_obj['width']) + r' x ' + str(file_obj['height'])

                # 帧率模式
                media_data['v_frame_rate_mode'] = str(file_obj['width']) + r' x ' + str(file_obj['height'])

                frame_rate_mode = file_obj['frame_rate_mode']
                if 'CFR' == frame_rate_mode:
                    media_data['v_frame_rate_mode'] = 'CFR (恒定帧率)'
                elif 'VFR' == frame_rate_mode:
                    media_data['v_frame_rate_mode'] = 'VFR (可变帧率)'

                # 帧率
                media_data['v_frame_rate'] = file_obj['other_frame_rate'][0]

                # 码率
                bit_rate = file_obj['bit_rate']
                media_data['v_k_bit_rate'] = str(Decimal(int(bit_rate) / 1000).quantize(Decimal("0")))
                media_data['v_m_bit_rate'] = str(Decimal(int(bit_rate) / 1000 / 1000).quantize(Decimal("0.00")))
            # 音频信息
            elif 'Audio' == track_type:
                # 混响模式
                channel_s = file_obj['channel_s']
                if 2 == channel_s:
                    media_data['a_channel_type'] = 'Stereo (立体声)'
                else:
                    media_data['a_channel_type'] = '其它'

                # 音频格式
                media_data['a_commercial_name'] = file_obj['commercial_name'] + r' (' + file_obj['format_info'] + r')'

                # 音频采样率
                media_data['a_sampling_rate'] = file_obj['other_sampling_rate'][0]

                # 音频比特率
                media_data['a_bit_rate'] = file_obj['other_bit_rate'][0]
        media_data_list.append(media_data)
    return media_data_list


def mediainfo_(file_path: str):
    '''
    调用触发函数
    Args:
        file_path:给定的文件路径或文件夹路径.

    Returns:

    '''
    file_path_items = get_files_item(file_path)
    file_datas = mediainfo_handler(file_path_items)
    get_mediainfo(file_datas)
