# -*- coding:utf-8 -*-

if __name__ == '__main__':
    username, score = 'Java', 98
    # 传统 C 语言风格
    print('%s 成绩是 %d' % (username, score))

    # string.format 风格
    print('{}的成绩是：{}.'.format(username, score))

    # f-string 风格
    print(f'{username}的成绩是：{score}')
