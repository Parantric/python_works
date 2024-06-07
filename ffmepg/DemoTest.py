# -*- coding:utf-8 -*-
import ffmpeg as ff

if __name__ == '__main__':
    input_file_name = r'E:\Adobe_Home\Adobe_Project\作品导出目录\1080p.NEW.BDRip.Japanese.x264.人工精译简体中字.mp4'
    json = ff.probe(input_file_name)
    # print(json)
    ff.get_media_info(input_file_name)
