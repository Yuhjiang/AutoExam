import pandas as pd
import xlrd

path = r'E:\中建三局\文件\题库\技术部题库20180105'
columns = ['序号', '题目', '答案', '来源']


def read_excel_file(fpath):
    """
    读取excel文件
    :param fPath:
    :return:
    """
    data = xlrd.open_workbook(fpath)

    # TODO  增加多个读取多个sheet的功能
    table = data.sheets()[0]
    nrows = table.nrows

    index = []
    questions = []
    answers = []
    sources = []

    for i in range(1, nrows-1):
        row = table.row_values(i)
        index.append(row[0])
        questions.append(row[1])
        answers.append(row[2])
        sources.append(row[4] + row[5])

    pData['序号'] = index
    pData['题目'] = questions
    pData['答案'] = answers
    pData['来源'] = sources


file = '\DGTJ08-61-2010基坑工程技术规范.xlsx'
pData = pd.DataFrame(columns=columns)
read_excel_file(path+file)
sFile = 'collection.csv'
print(pData)
pData.to_csv(sFile, index=False)