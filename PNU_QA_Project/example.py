import re
import sourceCode.Table_Holder
from sourceCode import Table_Holder
from Utils.HTML_Utils import overlap_table_process
import numpy as np
from scipy.stats import rankdata

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
            if item.isnumeric() == False:
                table_data[i][j] = '0'
    print('___________________ int로 자료형 변환----------------')
    table_data = ([list(map(int,i)) for i in table_data])
    printTable(table_data,table_head)

    print('--------------랭킹 매기기-------------')
    #랭킹 매김
    # https: // stackoverflow.com / questions / 36193225 / numpy - array - rank - all - elements
    print(rankdata(table_data, axis=0,method='min',min=0))

    # numpy_table_data = np.array(table_data)
    # numpy_table_data = (numpy_table_data.argsort(axis=0)).argsort(axis=0)
    # table_data = numpy_table_data.tolist()
    # printTable(table_data,table_head)

    return


table_holder = Table_Holder.Holder()
file = open('test.html', 'r', encoding='utf-8')
table_text = file.read()
table_text, overlap_table_texts = overlap_table_process(table_text=table_text)

table_holder.get_table_text(table_text=table_text)
table_data = table_holder.table_data
table_head = table_holder.table_head

printTable(table_data, table_head)
numberToRanking(table_data,table_head)





