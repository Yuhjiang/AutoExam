# -*- coding=utf-8 -*-
"""
Module:     utils
Summary:    常用工具
Author:     Yuhao Jiang
Created:    2018/10/31
Updated:    2018/10/31 Ver 1.0 判断题目对错
"""
import jieba
from gensim import models
import numpy as np
from scipy.linalg import norm
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import logging

jieba.setLogLevel(logging.INFO)

model_file = r'E:\Program\Python\NLP\word2vec\news_12g_baidubaike_20g_novel_90g_embedding_64.bin'
model = models.KeyedVectors.load_word2vec_format(model_file, binary=True)


def similarity_tf_idf(answer_doc, true_doc):
    """
    利用tf-idf分析相似度
    :param answer_doc: 回答文本
    :param true_doc: 正确答案文本
    :return:
    """
    def add_space(s):
        new_s = [word for word in jieba.cut(s)]
        return ' '.join(list(new_s))

    s1, s2 = add_space(answer_doc), add_space(true_doc)

    cv = TfidfVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1, s2]
    vectors = cv.fit_transform(corpus).toarray()
    return np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))


def similarity_word2vec(answer_doc, true_doc):
    """
    利用百度文库训练好的模型，计算相似度
    :param answer_doc: 回答文本
    :param true_doc: 正确答案文本
    :return:
    """
    answer_doc, true_doc = data_clean(answer_doc), data_clean(true_doc)

    def sentence_vector(s):
        words = jieba.lcut(s)
        v = np.zeros(64)
        for word in words:
            v += model[word]
        v /= len(words)
        return v

    v1, v2 = sentence_vector(answer_doc), sentence_vector(true_doc)
    return np.dot(v1, v2) / (norm(v1) * norm(v2))


def data_clean(doc):
    """
    清洗数据，去除标点符号
    :param doc:
    :return:
    """
    string = re.findall(u'[\u4e00-\u9fa5]+', doc)

    return string


def generate_name(doc_name):
    """
    生成规范名，只包含字母数字，如GB20202-2002
    :param doc_name:
    :return:
    """
    doc_name = doc_name.replace('－', '-')
    doc_name = doc_name.replace(' ', '')
    ind = doc_name.find('-', 1)
    name = doc_name[:ind+5]
    return name


if __name__ == '__main__':
    s1 = '工程概况 风险因素分析 施工方法和施工工艺 基坑与周边环境安全保护 组织管理措施 施工安全技术措施' \
         '变形控制指标 工程危险控制重点与难点'
    s2 = '1  工程概况；2  工程地质与水文地质条件；3  风险因素分析；4  ' \
         '工程危险控制重点与难点；5  施工方法和主要施工工艺；6  基坑与周边环境安全保护要求；7  ' \
         '监测实施要求；8  变形控制指标与报警值；9 ' \
         ' 施工安全技术措施；10  应急方案；11  组织管理措施。'
    print(similarity_tf_idf(s1, s2))