# -*- coding=utf-8 -*-
"""
Module:     random_select
Summary:    随机出题
Author:     Yuhao Jiang
Created:    2018/10/30
Updated:    2018/10/30 Ver 1.0 在命令行随机出题
Todo:       根据配置文件选择出题方式
"""
import pandas as pd
import numpy as np
import sys


def random_select(fpath):
    data = pd.read_csv(fpath)

    end = ''
    while end != ':quit' and end != ':q':
        row = data.sample(n=1)
        index, number, question, answer, source, typen = row.iloc[0]
        # 输出题目
        print(question)
        ans = input('输入答案：')
        if ans == answer:
            print('回答正确')
        else:
            print('回答错误')
            print('正确答案：{}\n来源：{}'.format(answer, source))
        end = input()


if __name__ == '__main__':
    fpath = sys.argv[1]
    random_select('{}.csv'.format(fpath))