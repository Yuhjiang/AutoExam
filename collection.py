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
import xlwt
import sys
from utils import generate_name
import json

columns = ['序号', '题目', '答案', '来源', '题型']
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

        for i in range(1, nrows):
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

    excel_data = {
        'index': index,
        'questions': questions,
        'answers': answers,
        'sources': sources,
        'types': types,
    }

    return excel_data


def create_csv():
    """
    创建汇总所有题目的csv文件
    :return:
    """
    with open('collection.json', 'r', encoding='utf-8') as load_f:
        settings = json.load(load_f)
    exam_repos = [excel for excel in settings['list']]
    index = []
    questions = []
    answers = []
    sources = []
    types = []
    for exam_repo in exam_repos:
        excel_data = read_excel_file(settings['index'] + exam_repo + '.xlsx')
        index += excel_data['index']
        questions += excel_data['questions']
        answers += excel_data['answers']
        sources += excel_data['sources']
        types += excel_data['types']

    pdata = pd.DataFrame(columns=columns)

    pdata['序号'] = index
    pdata['题目'] = questions
    pdata['答案'] = answers
    pdata['来源'] = sources
    pdata['题型'] = types
    pdata.to_csv('collection.csv')


def create_excel():
    """
    创建汇总所有题目的excel文件
    :return:
    """
    pdata = pd.read_csv('collection.csv', index_col=0)

    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
    borders = xlwt.Borders()
    borders.left = xlwt.Borders.MEDIUM
    style2 = xlwt.XFStyle()
    style2.alignment = alignment

    alignment.vert = xlwt.Alignment.VERT_CENTER
    style = xlwt.XFStyle()
    style.alignment = alignment

    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('题目')

    worksheet.write(0, 0, label='序号', style=style)
    worksheet.write(0, 1, label='题型', style=style)
    worksheet.write(0, 2, label='题目', style=style)
    worksheet.write(0, 3, label='答案', style=style)
    worksheet.write(0, 6, label='答案', style=style)

    data = pdata.sample(frac=1).reset_index(drop=True)
    with open('collection.json', 'r', encoding='utf-8') as load_f:
        settings = json.load(load_f)
        types = settings['type']

    ind = 0
    for i, row in data.iterrows():
        if row['题型'] in types:
            ind += 1
            worksheet.write(ind, 0, label=str(i+1), style=style)
            worksheet.write(ind, 1, label=row['题型'], style=style)
            worksheet.write(ind, 2, label=row['题目'], style=style2)
            worksheet.write(ind, 6, label=row['答案'], style=style2)
    workbook.save('exam.xls')


if __name__ == '__main__':
    create_csv()
    create_excel()