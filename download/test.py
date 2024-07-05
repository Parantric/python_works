# -*- coding:utf-8 -*-
# -*- coding: utf-8 -*-
import base64
import json
import os
import time

import ddddocr
import requests

from PIL import Image
from fontTools.misc.transform import Offset
from fontTools.ttLib import TTFont
from fontTools.pens.freetypePen import FreeTypePen
import matplotlib.pyplot as plt
from paddleocr import PaddleOCR
import logging


# 拆解woff2文件，保存为单个字体图片:保存至 imgs 文件夹
def font_split_single_img():
    # 解析字体文件
    font = TTFont(r'F:\Home\Users\renjy\Desktop\dc027189e0ba4cd-700.woff2')  # woff2文件
    cmap = font.getBestCmap()
    # font.saveXML('font.xml')  # 保存存为xml
    index = 1
    for n, v in cmap.items():
        pen = FreeTypePen(None)  # 实例化Pen子类
        d = v
        glyph = font.getGlyphSet()[d]  # 通过字形名称选择某一字形对象
        glyph.draw(pen)  # “画”出字形轮廓
        plt.axis('off')  # 禁用坐标轴
        width, ascender, descender = glyph.width, font['OS/2'].usWinAscent, -font['OS/2'].usWinDescent  # 获取字形的宽度和上沿以及下沿
        height = ascender - descender  # 利用上沿和下沿计算字形高度
        # pen.show(width=width, height=height, transform=Offset(0, -descender))  # 显示以及矫正
        b = pen.array(width=width, height=height, transform=Offset(0, -descender), contain=True)
        # print(index, '/', len(cmap), '~~~', glyph)
        fig = plt.figure()
        plt.imshow(b)
        plt.axis('off')  # 禁用坐标轴
        os.makedirs('imgs', exist_ok=True)
        # 可以设置生成图片的背景颜色等 savefig("trial_fig.png", facecolor='red') # Here the facecolor is red.
        # plt.savefig('./imgs/{0}.jpg'.format(d),facecolor=fig.get_facecolor(), edgecolor='none')
        plt.savefig('./imgs/{0}.jpg'.format(d),facecolor='#440053')
        # plt.show()    # 显示
        plt.clf()
        plt.cla()
        plt.close()
        index += 1


# 用 ddddocr 识别图片文字,保存至 imgs_copy_word 文件夹
def ocrWords():
    ocr = ddddocr.DdddOcr()  # 识别
    word_map = {}
    for parent, dirnames, filenames in os.walk('imgs'):  # 遍历每一张图片
        for filename in filenames:
            k = filename.split('.')[0]
            currentPath = os.path.join(parent, filename)
            with open(currentPath, 'rb') as f:
                image = f.read()
            res = ocr.classification(image)
            if len(res) == 0:
                res = '未找到'
            if len(res) > 1:
                res = res[0]
            print(k, ':', res)
            os.makedirs('imgs_copy_word', exist_ok=True)
            d = f'{k}__{res}.jpg'
            img = Image.open(currentPath)
            img.save('imgs_copy_word/%s' % d)
            word_map[k] = res


# 用 ddddocr 识别图片文字,保存至 imgs_copy_word 文件夹
def ocrWords_paddleOCR():
    ocr = PaddleOCR()  # 识别
    word_map = {}
    for parent, dirnames, filenames in os.walk('imgs'):  # 遍历每一张图片
        for filename in filenames:
            k = filename.split('.')[0]
            currentPath = os.path.join(parent, filename)
            # with open(currentPath, 'rb') as f:
            #     image = f.read()
            res = ocr.ocr(currentPath, cls=True)

            if res[0] is None:
                result = '未找到'
            else:
                result = res[0][0][-1][0]
            print(k, ':', result)
            os.makedirs('imgs_copy_word', exist_ok=True)
            d = f'{k}__{result}.jpg'
            img = Image.open(currentPath)
            img.save('imgs_copy_word/%s' % d)
            word_map[k] = res


# 根据识别后的名称，提取结果，并保存为 .json文件：dddddocr识别的保存为：ocr_dddd.json,百度ocr识别的，保存为：ocr_baidu.json
def readImagName(imagesPath='imgs_copy_word', saveJsonName='ocr_dddd.json'):
    word_map = {}
    for parent, dirnames, filenames in os.walk(imagesPath):  # 遍历每一张图片
        for filename in filenames:
            k = filename.split('.')[0]
            res = k.split('__')[1]
            word_map[k.split('__')[0]] = res
    if word_map:
        with open(saveJsonName, 'w', encoding='utf-8') as f:
            f.write(json.dumps(word_map, ensure_ascii=False))


# 用 百度ocr接口解析图片，保存至 imgs_copy_word_bdu 文件夹
def ocrWords_baidu_ocr():
    url = 'https://ai.baidu.com/aidemo'
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": 'BAIDUID=D7FF1AB8471A40E8DF8B53FE2FC146AA:FG=1; BAIDUID_BFESS=D7FF1AB8471A40E8DF8B53FE2FC146AA:FG=1; __bid_n=1903bfd2f501376314d0af; BIDUPSID=D7FF1AB8471A40E8DF8B53FE2FC146AA; PSTM=1719868244; H_PS_PSSID=60336_60359; ZFY=I:A6cX9xCC:AnbnUv27:BMJ1BxTSfXV0CghTvhwCdwY6nA:C; RT="z=1&dm=baidu.com&si=50170bf2-8edb-4e6e-8440-1e1a45fb14ff&ss=ly776593&sl=4&tt=2t4&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=4su&ul=bpa&hd=bpf"; CAMPAIGN_TRACK=; ucbearer-clientid=; bce-login-userid=; bce-device-token=; SIGNIN_UC=; __cas__id__285=; bce-device-cuid=; __cas__rn__=; ucbearer-token=; bce-verify-status=; CAMPAIGN_TRACK_TIME=; __cas__st__285=; ucbearer-ucid=; ucbearer-devicecode=; BDUSS=Uo0anVzWEhnMWR6Y2U0Tk1KWWFTZkN1bTVZZ1dwTGl-ekdKR29oSTBNaXhuYTltRVFBQUFBJCQAAAAAAAAAAAEAAACxZmXEtPPBfbK7us0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALEQiGaxEIhmU; BDUSS_BFESS=Uo0anVzWEhnMWR6Y2U0Tk1KWWFTZkN1bTVZZ1dwTGl-ekdKR29oSTBNaXhuYTltRVFBQUFBJCQAAAAAAAAAAAEAAACxZmXEtPPBfbK7us0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALEQiGaxEIhmU; bce-sessionid=00117bcc784e38c45128abdced0a569237e; bceAccountName=PASSPORT:3294979761; bce-ctl-client-cookies="BDUSS,bce-passport-stoken,bce-device-cuid,bce-device-token,BAIDUID"; bce-passport-stoken=e830c67547da9b3bb84cc68be51c9f2e5c46e8b65b5b1d27ea29c6ff69cbe22a; bce-user-info=2024-07-05T23:26:43Z|7f69aa9e4dd9230065fd2406005244ff; bce-ctl-sessionmfa-cookie=bce-session; bce-session=0bf7d5fa47a946caa741b818c1c40c88c3ac1222b00e4018abb56165901372a1|43f4582e92d011d6552fd13873661a3f; bce-login-display-name=%E5%A4%A7%E7%BE%AE%E4%B8%8D%E5%92%8C; bce-userbind-source=PASSPORT; bce-auth-type=PASSPORT; bce-login-type=PASSPORT; bce-login-expire-time="2024-07-05T15:56:43Z|319d987b3cd1691e3818fe285a43fafd"; loginUserId=3294979761',
        "Host": "ai.baidu.com",
        # "Referer": "undefined",
        'Referer': 'https://cloud.baidu.com/product/ocr/general',  # 通用文字识别接口，高精度不带位置
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

    word_map = {}
    index = 0
    for parent, dirnames, filenames in os.walk('imgs'):  # 遍历每一张图片
        for filename in filenames:
            index += 1
            # if index <= 332:
            #     continue
            k = filename.split('.')[0]
            currentPath = os.path.join(parent, filename)
            with open(currentPath, 'rb') as f:
                image = f.read()
            bs64Img = base64.b64encode(image)
            bs64Img = 'data:image/jpeg;base64,%s' % bs64Img.decode()
            postData = {
                "image": bs64Img,
                "image_url": "",
                "type": "https://aip.baidubce.com/rest/2.0/ocr/v1/webimage"
            }
            response = requests.post(url=url, headers=headers, data=postData)
            content = json.loads(response.text.strip())
            if content['msg'] == 'success':
                if int(content['data']['words_result_num']) == 0:
                    res = '未找到Result0'
                else:
                    res = content['data']['words_result'][0]['words']
            else:
                res = '未找到'
            print(k, 'res:', res, index, len(filenames))
            os.makedirs('imgs_copy_word_bdu', exist_ok=True)
            d = f'{k}__{res}.jpg'
            img = Image.open(currentPath)
            img.save('imgs_copy_word_bdu/%s' % d)
            word_map[k] = res
            time.sleep(0.4)


if __name__ == '__main__':
    logging.disable(logging.DEBUG)  # 关闭DEBUG日志的打印
    logging.disable(logging.WARNING)  # 关闭WARNING日志的打印

    # font_split_single_img()
    # ocrWords()
    # ocrWords_baidu_ocr()
    # ocrWords_paddleOCR()
    readImagName(r'E:\workspace_home\coding_home\python_code\python_works\download\imgs_copy_word')
