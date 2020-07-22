from HTML_Utils import get_table_head
import re
import Table_Holder
from HTML_Utils import get_table_head
from HTML_Utils import overlap_table_process
import numpy as np

table_holder = Table_Holder.Holder()

file = open('test.html', 'r', encoding='utf-8')
table_text = file.read()

table_text, overlap_table_texts = overlap_table_process(table_text=table_text)

table_holder.get_table_text(table_text=table_text)
table_data = table_holder.table_data

for data in table_data:
    print(data)