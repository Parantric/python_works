# -*- coding:utf-8 -*-
class MediaException(Exception):
    def __init__(self, msg):
        super().__init__(self)
        self.msg = msg
