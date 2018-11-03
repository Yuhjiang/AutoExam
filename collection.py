# -*- coding=utf-8 -*-
"""
Module:     collection
Summary:    收集所有题库的题目，并保存到csv
Author:     Yuhao Jiang
Created:    2018/10/30
Updated:    2018/10/30 Ver 1.0 收集所有数据
"""
import pandas as pd
import xlrd
import sys
import utils

path = r'E:\中建三局\文件\题库\技术部题库20180105'
columns = ['序号', '题目', '答案', '来源', '题型']
pdata = pd.DataFrame(columns=columns)
judge_answer = {
    '√': 'T',
    '×': 'F',
}


def read_excel_file(fpath):
    """
    读取excel文件
    :param fPath:
    :return:
    """
    data = xlrd.open_workbook(fpath)

    index = []
    questions = []
    answers = []
    sources = []
    types = []
    for table in data.sheets():
        nrows = table.nrows

        for i in range(1, nrows-1):
            row = table.row_values(i)
            if row[1] == '':
                continue
            index.append(row[0])
            questions.append(row[1])
            if table.name == '判断题':
                answers.append(judge_answer.get(row[2], ''))
            else:
                answers.append(row[2])
            sources.append(row[4] + row[5])
            types.append(table.name)

    pdata['序号'] = index
    pdata['题目'] = questions
    pdata['答案'] = answers
    pdata['来源'] = sources
    pdata['题型'] = types


if __name__ == '__main__':
    fpath = path + '\\' + sys.argv[1] + '.xlsx'
    # fpath = path + '\\' + 'GB50202-2002建筑地基基础工程施工质量验收规范.xlsx'
    read_excel_file(fpath)
    csv_name = utils.generate_name(sys.argv[1])
    pdata.to_csv(csv_name + '.csv')
