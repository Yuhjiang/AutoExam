# -*- coding=utf-8 -*-
"""
Module:     utils
Summary:    常用工具
Author:     Yuhao Jiang
Created:    2018/10/31
Updated:    2018/10/31 Ver 1.0 判断题目对错
"""
import jieba
from gensim import models, similarities, corpora
import numpy as np
from scipy.linalg import norm
from sklearn.feature_extraction.text import TfidfVectorizer
import re


# model_file = r'E:\Program\Python\NLP\word2vec\news_12g_baidubaike_20g_novel_90g_embedding_64.bin'
# model = models.KeyedVectors.load_word2vec_format(model_file, binary=True)


def similarity_tf_idf(answer_doc, true_doc):
    """
    利用tf-idf分析相似度
    :param answer_doc: 回答文本
    :param true_doc: 正确答案文本
    :return:
    """
    def add_space(s):
        return ' '.join(list(s))

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
    string = re.sub('[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）()\[\]]+', '', doc)

    return string