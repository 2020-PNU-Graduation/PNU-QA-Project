import re
import sourceCode.Table_Holder
from sourceCode import Table_Holder
from Utils.HTML_Utils import overlap_table_process
import numpy as np
from scipy.stats import rankdata
from numpy import transpose

def checkEqual3(lst):
   return lst[1:] == lst[:-1]

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def printTable(table_data, table_head):
    print(table_head)
    for data in table_data:
        print(data)
    return


def numberToRanking(table_data, table_head):
    # 비교 가능한 칼럼(숫자타입)을 찾는다. 비교가 불가능하면 '0'으로 바꾼다.
    print('--------------비교불가능한 칼럼 0 처리-------------')
    i = -1
    for col in table_data:
        i = i + 1
        j = -1
        for item in col:
            j = j + 1
            # 추후에 조건 예를들어 추가 km 같은 단위표현
            if RepresentsInt(item) == False:
                table_data[i][j] = '-1'
    print('___________________ int로 자료형 변환----------------')
    table_data = ([list(map(int,i)) for i in table_data])
    printTable(table_data,table_head)

    print('--------------랭킹 매기기-------------')
    arr = table_data
    arrCol = []
    arrResult = []
    # 같은 랭크는 같은 weight 이고 한칸 띄운다.
    # 비교 안되는 원하는 칼럼은 다 0으로
    for i in range(0, len(arr[0])):
        for j in range(0, len(arr)):
            arrCol.append(arr[j][i])
        # rank the array and apply
        sortedCol = [sorted(arrCol).index(x) + 1 for x in arrCol]
        print(sortedCol)
        if checkEqual3(sortedCol):
            sortedCol[:len(sortedCol)] = [0] * len(sortedCol)
        arrResult.append(sortedCol)
        print()
        arrCol.clear()

    # arrResult = list(map(list, zip(arrResult)))
    arrResult = transpose(arrResult)
    print(arrResult)
    return

table_holder = Table_Holder.Holder()
file = open('tableExampleHTMLCode/test.html', 'r', encoding='utf-8')
table_text = file.read()
table_text, overlap_table_texts = overlap_table_process(table_text=table_text)

table_holder.get_table_text(table_text=table_text)
table_data = table_holder.table_data
table_head = table_holder.table_head

printTable(table_data, table_head)
numberToRanking(table_data,table_head)





