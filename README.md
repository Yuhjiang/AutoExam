# AutoExam
用于学习题库的程序
[TOC]
# collection.py
- 收集指定文件的所有题目，并保存到一个文件中，方便后续从该文件中出题

## **TODO**:
1. 添加配置文件，根据配置文件选择文件以及保存的格式等等功能
2. 解决文件命名格式不统一导致生成文件命名错误的问题
3. 解决excel文件空白行导致random_select.py出错的问题

# random_select.py
- 选择指定的题库文件(.csv)，随机出题

**TODO**:扩展功能，增加出题生成excel文件功能，并提供批改功能

# utils.py
## similarity_tf_idf(my_answer, right_answer)
- 利用tf-idf算法分析填空题和简答题答案正确性
- 受先用jieba分词，再用scipy提供的tf-idf算法

## similarity_word2vec(my_answer, right_answer)
- 利用百度文库训练好的模型
- 存在局限性，无法分析带有非中文的答案，虽然目前将过滤后答案的用于计算相似度，但不建议作为主要计算方式

## data_clean(doc)
- 清洗答案中的非中文数据
