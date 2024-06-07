# -*- coding:utf-8 -*-
import os.path

import ffmpeg
from decimal import Decimal

VIDEO_TYPE_MKV = 'Matroska / WebM'


def get_data_items(json_data):
    '''
    Args:
        msg:json 对象

    Returns:包含必要信息的对象

    '''
    # 获取视频信息列表
    media_data = json_data.get('streams')[0]
    media_format_data = json_data.get('format')
    # 获取音频信息列表
    audio_data = json_data.get('streams')[1]

    # 视频编码规则短名称
    codec_name = media_data.get('codec_name')
    # 视频编码规则全称
    codec_long_name = media_data.get('codec_long_name')

    # 分辨率
    width = media_data.get('width')
    height = media_data.get('height')
    resolution = str(width) + r' x ' + str(height)

    # 获取视频类型
    video_type = media_format_data.get('format_long_name')
    bit_rate = ''
    k_bit_rate = ''
    if video_type == VIDEO_TYPE_MKV:
        # 帧率
        r_frame_rate = media_data.get('r_frame_rate')
    else:
        # 帧率
        r_frame_rate = media_data.get('r_frame_rate')
        r_frame_rate = r_frame_rate.split('/')[0]

        # 比特率（码率）
        bit_rate = media_data.get('bit_rate')
        k_bit_rate = int(bit_rate) / 1000
        bit_rate = k_bit_rate / 1000

        k_bit_rate = str(Decimal(k_bit_rate).quantize(Decimal("0")))
        bit_rate = str(Decimal(bit_rate).quantize(Decimal("0.00")))

    # 总比特率
    total_bit_rate = media_format_data.get('bit_rate')

    k_total_bit_rate = int(total_bit_rate) / 1000
    total_bit_rate = k_total_bit_rate / 1000

    k_total_bit_rate = str(Decimal(k_total_bit_rate).quantize(Decimal("0")))
    total_bit_rate = str(Decimal(total_bit_rate).quantize(Decimal("0.00")))

    file_name = media_format_data.get('filename')
    file_name = os.path.basename(file_name)

    # 音频编码名称
    audio_codec_name = audio_data.get('codec_name')
    # 音频编码规则全称
    audio_codec_long_name = audio_data.get('codec_long_name')
    # 混音模式
    audio_channel_layout = audio_data.get('channel_layout')
    # 音频采样率
    audio_sample_rate = audio_data.get('sample_rate')
    # 音频比特率
    audio_bit_rate = audio_data.get('bit_rate')

    if audio_bit_rate is None:
        audio_bit_rate = 'Auto'
    else:
        audio_bit_rate = str(Decimal(int(audio_bit_rate) / 1000).quantize(Decimal("0")))

    return {
        'codec_long_name': codec_long_name,
        'resolution': resolution,
        'bit_rate': bit_rate,
        'k_bit_rate': k_bit_rate,
        'total_bit_rate': total_bit_rate,
        'k_total_bit_rate': k_total_bit_rate,
        'file_name': file_name,
        'r_frame_rate': r_frame_rate,
        'audio_codec_long_name': audio_codec_long_name,
        'audio_sample_rate': audio_sample_rate,
        'audio_channel_layout': audio_channel_layout,
        'audio_bit_rate': audio_bit_rate,
    }


def probe_media(file_name):
    '''

    Args:
        file_name:

    Returns:

    '''
    msg = ffmpeg.probe(file_name)
    # 查看 JSON 完整对象 测试用
    # print(msg)
    items = get_data_items(msg)
    print(items['file_name'])
    print('编码格式:', items['codec_long_name'])
    print('分辨率:', items['resolution'])
    print('帧率:', items['r_frame_rate'], '帧/秒')
    print('混音模式:', items['audio_channel_layout'])
    print('音频格式:', items['audio_codec_long_name'])
    print('音频采样率:', items['audio_sample_rate'])

    if items['audio_bit_rate'] == 'Auto':
        print('音频比特率:', items['audio_bit_rate'])
    else:
        print('音频比特率:', items['audio_bit_rate'], 'Kbps')

    if items['bit_rate'] != '':
        print('数据速率(Kbps):', items['k_bit_rate'])
        print('数据速率(Mbps):', items['bit_rate'])
        print('')
    print('总比特率(Kbps):', items['k_total_bit_rate'])
    print('总比特率(Mbps):', items['total_bit_rate'])
    print('---------------------------------------------------------------------')


if __name__ == '__main__':
    # media_path = r'F:\Home\Users\renjy\Videos\绝世武魂\demo'
    media_path = r'E:\temp_transfer\ali_cloudy\阿里云盘Open\=================\绝世武魂\377.mkv'

    if '\\' in media_path:
        media_path = media_path.replace('\\', '/')
    if os.path.exists(media_path):
        print('---------------------------------------------------------------------')
        if os.path.isdir(media_path):
            files = os.listdir(media_path)
            for file in files:
                file_extension = os.path.splitext(file)[-1]
                if file_extension in ['.mp4', '.MP4', '.mkv', '.MKV', '.avi', '.AVI', ]:
                    media_file = os.path.join(media_path, file)
                    probe_media(media_file)
        else:
            probe_media(media_path)
    else:
        print('【' + media_path + '】' + '路径不存在...')
