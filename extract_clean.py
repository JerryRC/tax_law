import os
import re

SAVE_PATH = './sentences'
EXCLUDE_LIST = ['', '注释：', '网站纠错']


def check_null(f):
    '''检查文本是否为空'''
    with open(f, 'r', newline='') as fin:
        empty = 1
        for line in fin.readlines():
            if line.strip() != '':
                empty = 0
                break
        if empty:
            print(f + ' is empty')


def extract(f):
    '''抽取政策文本中的句子'''
    if f[0] > '9' or f[0] < '0':
        return

    sentences = []
    with open(f, 'r', encoding='utf-8', newline='') as fin:
        for line in fin.readlines():
            line = line.strip()
            if line in EXCLUDE_LIST or '附件' in line:
                continue
            line = re.sub('[\s]+', '\n',
                          line)  # 正式中文文本是没有(连续)空格的, 以此判断是<br>的换行
            sens = re.split('([。])', line)  # 保留分隔符分割
            sens.append('')
            sens = [''.join(s) for s in zip(sens[0::2], sens[1::2])]
            if sens[-1].strip() == '':  # 分句保留符号会在最后落下空串
                sens.pop()
            sentences += sens

    if sentences.__len__() == 0:
        return

    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)
    file_path = SAVE_PATH + '/' + re.sub('[_origin.txt]', '', f)
    for i in range(sentences.__len__()):
        filename = file_path + '_{}.txt'.format(i)
        with open(filename, 'w', encoding='utf-8') as fout:
            fout.write(sentences[i])


def walk_txt():
    '''游走txt文本'''
    # os.chdir('./sentences')
    for f in os.listdir():
        if os.path.isfile(f) and f[-4:] == '.txt':
            # check_null(f)
            extract(f)


if __name__ == '__main__':
    walk_txt()
