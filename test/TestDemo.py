import subprocess, json


class FFprobe():
    def __init__(self):
        self.filepath = ''
        self._video_info = {}

    def parse(self, filepath):
        self.filepath = filepath
        try:
            res = subprocess.check_output(
                ['ffprobe', '-i', self.filepath, '-print_format', 'json', '-show_format', '-show_streams', '-v',
                 'quiet'])
            res = res.decode('utf8')
            self._video_info = json.loads(res)
            print('_video_info ',self._video_info)
        except Exception as e:
            print(e)
            raise Exception('获取视频信息失败')

    def video_width_height(self):
        streams = self._video_info['streams'][0]
        return (streams['width'], streams['height'])

    def video_filesize(self, format='gb'):
        v_format = self._video_info['format']
        size = int(v_format['size'])
        kb = 1024
        mb = kb * 1024
        gb = mb * 1024
        tb = gb * 1024
        if size >= tb:
            return "%.1f TB" % float(size / tb)
        if size >= gb:
            return "%.1f GB" % float(size / gb)
        if size >= mb:
            return "%.1f MB" % float(size / mb)
        if size >= kb:
            return "%.1f KB" % float(size / kb)

    def video_full_frame(self):
        stream = self._video_info['streams'][0]
        return stream['nb_frames']

    def video_time_length(self):
        v_format = self._video_info['format']
        return str(int(float(v_format['duration']) / 3600)).__add__('小时').__add__(
            str(int(float(v_format['duration']) % 3600 / 60))).__add__('分钟')

    def video_info(self):
        item = {
            'path': self.filepath,
            'height_width': self.video_width_height(),
            'filesize': self.video_filesize(),
            'time_length': self.video_time_length()
        }
        print('item = ', item)
        return item


if __name__ == "__main__":
    ffprobe = FFprobe()
    ffprobe.parse(
        r'E:\temp_transfer\ali_cloudy\阿里云盘Open\=================\绝世武魂\377.mkv')
    print(ffprobe.video_info())
