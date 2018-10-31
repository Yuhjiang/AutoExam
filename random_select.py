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
import utils


def random_select(fpath):
    data = pd.read_csv(fpath)

    end = ''
    while end != ':quit' and end != ':q':
        row = data.sample(n=1)
        index, number, question, answer, source, typen = row.iloc[0]
        # 输出题目
        print(question)
        ans = input('输入答案：')
        result = judgement(ans, answer, typen)
        if result[0] > 0:
            print(result[1])
        else:
            print(result[1])
            print('正确答案：{}\n来源：{}'.format(answer, source))
        end = input()


def judgement(my_answer, true_answer, question_type, word2vec=False):
    """
    判断答案对错
    :param my_answer:
    :param true_answer:
    :param type:    问题类型
    :param word2vec:
    :return:
    """
    result = (-1, '回答错误')
    if question_type in ['单项选择', '多项选择', '判断题']:
        if my_answer == true_answer:
            result = (1, '回答正确')
    else:
        sim1 = 0
        sim2 = 0
        try:
            sim1 = utils.similarity_word2vec(my_answer, true_answer)
        except:
            sim2 = utils.similarity_tf_idf(my_answer, true_answer)
        finally:
            grade = max(sim1, sim2)
        if grade >= 0.8:
            result = (1, '非常正确')
        elif 0.6 < grade < 0.8:
            result = (0.7, '勉强正确')
        elif 0.4 < grade <= 0.6:
            result = (0.5, '还行吧……')
        else:
            result = (-1, '答案错误')
    return result


if __name__ == '__main__':
    fpath = sys.argv[1]
    random_select('{}.csv'.format(fpath))