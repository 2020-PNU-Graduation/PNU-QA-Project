from HTML_Utils import *
import os
import json
import os

from sourceCode import tokenization
import numpy as np

from sourceCode import Chuncker


chuncker = Chuncker.Chuncker()

max_length = 450

path_dir = 'F:\\korquad2_data'

sequence_has_ans = np.zeros(shape=[80000 * 2, max_length], dtype=np.int32)
segments_has_ans = np.zeros(shape=[80000 * 2, max_length], dtype=np.int32)
mask_has_ans = np.zeros(shape=[80000 * 2, max_length], dtype=np.int32)
answer_span = np.zeros(shape=[80000 * 2, 2], dtype=np.int32)
paragraph_type = np.zeros(shape=[80000 * 2], dtype=np.int32)

sequence_has_ans_z = np.zeros(shape=[80000 * 2, 3, max_length], dtype=np.int32)
segments_has_ans_z = np.zeros(shape=[80000 * 2, 3, max_length], dtype=np.int32)
mask_has_ans_z = np.zeros(shape=[80000 * 2, 3, max_length], dtype=np.int32)

file_list = os.listdir(path_dir)
file_list.sort()

file_list.pop(len(file_list) - 1)
file_list.pop(len(file_list) - 1)

print(file_list)
data_num = 0

vocab = tokenization.load_vocab(vocab_file='html_mecab_vocab_128000.txt')
tokenizer = tokenization.WordpieceTokenizer(vocab=vocab)

count = 0
false_count = 0
false_count2 = 0

cor = 0
wrong_case = 0

for file_name in file_list:

    print(file_name, 'processing....', data_num)

    in_path = path_dir + '\\' + file_name
    data = json.load(open(in_path, 'r', encoding='utf-8'))

    for article in data['data']:
        doc = str(article['context'])

        print(count, false_count, false_count2, file_name)

        for qas in article['qas']:
            error_code = -1

            answer = qas['answer']
            answer_start = answer['answer_start']
            answer_text = answer['text']
            question = qas['question']

            chuncker.get_feautre(query=question)

            query_tokens = []
            query_tokens.append('[CLS]')
            q_tokens = tokenizer.tokenize(question.lower())
            for tk in q_tokens:
                query_tokens.append(tk)
            query_tokens.append('[SEP]')

            doc_ = list(doc)

            ans1 = ''
            ans2 = ''

            ###부정확한 케이스는 제거
            right_case = True

            if len(doc) < answer_start + len(answer_text):
                right_case = False
                error_code = 1

            if len(doc) < answer_start:
                right_case = False
                error_code = 1
            ###

            ######
            # 정답에 ans 토큰을 임베딩하기 위한 코드
            ######
            if len(answer_text) > 1 and right_case is True:

                if doc[answer_start - 1] == ' ':
                    doc_ = doc[0: answer_start] + ' [answer] ' + answer_text + doc[answer_start + len(answer_text): -1]
                else:
                    doc_ = doc[0: answer_start] + ' [answer]' + answer_text + doc[answer_start + len(answer_text): -1]

            else:
                right_case = False
                error_code = 3
            ########

            ########
            #html 태그를 전처리 하기 위한 코드
            ########
            if right_case is False:
                print('wrong case!!', error_code)
                wrong_case += 1

            if right_case is True:
                doc_, table_list = pre_process_document(doc_, answer_setting=False, a_token1=ans1, a_token2=ans2,
                                                        td_setting=True)

                doc_ = doc_.replace('[a]', '')
                doc_ = doc_.replace('[/a]', '')
                doc_ = doc_.replace('[/li]', '')
                doc_ = doc_.replace('[/td]', '')
                doc_ = doc_.replace('[/th]', '')

                #######
                # 너무 긴 Token을 가지는 입력(512>)에 대해서 여러개의 입력으로 split 하는 코드입니다
                #######
                tokens = tokenizer.tokenize(doc_.lower())

                #get text seperated with tags
                ###
                #
                tagged_texts = []
                tabluar_texts = []

                seq = ''
                selected = -1

                for i in range(len(tokens)):
                    seq += tokens[i] + ' '

                    if (tokens[i] == '[/table]' or tokens[i] == '[/p]' or
                        tokens[i] == '[/list]' or tokens[i] == '##[/p]' or
                        tokens[i] == '##[/table]' or tokens[i] == '##[/list]') is True:

                        if seq.find('[answer]') != -1:
                            selected = len(tagged_texts)
                            answer_seq = seq

                        tagged_texts.append(seq.strip())
                        seq = ''
                ########

                i = 0
                while True:
                    if i >= len(tagged_texts):
                        break

                    if tagged_texts[i].find('table') == -1:
                        table_text = tagged_texts.pop(i)

                        # sequences.append(table_text)
                    else:
                        i += 1
                #
                ###
                selected = -1
                for i in range(len(tagged_texts)):
                    if tagged_texts[i].find('[answer]') != -1:
                        selected = i

                if selected == -1:
                    continue

                if tagged_texts[selected].find('[table]') == -1:
                    continue

                sequences = tagged_texts

                ch_scores = []

                for sequence in sequences:
                    if sequence.find('[answer]') == -1:
                        if sequence.find('[table]') != -1:
                            ch_scores.append(chuncker.get_chunk_score(paragraph=sequence) + 100)
                        else:
                            ch_scores.append(chuncker.get_chunk_score(paragraph=sequence))
                        #continue
                    else:
                        ch_scores.append(-9999)

                ch_scores = np.array(ch_scores, dtype=np.float32)
                #####

                for sequence in sequences:
                    if sequence.find('[answer]') == -1:
                        continue

                    for k in range(3):
                        zero_sequence = sequences[ch_scores.argmax()]
                        zero_sequence = zero_sequence.split('검색 ##하 ##러 가 ##기')[-1]
                        ch_scores[ch_scores.argmax()] -= 100
                        #print(zero_sequence)

                        tokens = []
                        segments_zero = []

                        tag_text = zero_sequence
                        tag_text = tag_text.replace('[/th]', '')
                        tag_text = tag_text.replace('[/td]', '')
                        tag_text = tag_text.replace('  ', ' ')
                        tag_text = tag_text.replace('  ', ' ')

                        tokens_ = zero_sequence.strip().split(' ')
                        for tk in query_tokens:
                            tokens.append(tk)
                            segments_zero.append(0)
                        for tk in tokens_:
                            tokens.append(tk)
                            segments_zero.append(1)

                        ids_zero = tokenization.convert_tokens_to_ids(tokens=tokens, vocab=vocab)
                        length = len(ids_zero)
                        if length > max_length:
                            length = max_length
                        for j in range(length):
                            sequence_has_ans_z[count, k, j] = ids_zero[j]
                            segments_has_ans_z[count, k, j] = segments_zero[j]
                            mask_has_ans_z[count, k, j] = 1

                    tag_text = sequence.split('검색 ##하 ##러 가 ##기')[-1]

                    tag_text = tag_text.replace('[/th]', '')
                    tag_text = tag_text.replace('[/td]', '')
                    tag_text = tag_text.replace('[answer]', '')
                    tag_text = tag_text.replace('[/answer]', '')

                    tag_text = tag_text.replace('  ', ' ')
                    tag_text = tag_text.replace('  ', ' ')
                    #print(tag_text)
                    #input()
                    tokens = []
                    segments = []

                    tokens_ = tag_text.strip().split(' ')
                    for tk in query_tokens:
                        tokens.append(tk)
                        segments.append(0)
                    for tk in tokens_:
                        if tk == '[answer]':
                            start_idx = len(tokens)
                        elif tk == '[/answer]':
                            stop_idx = len(tokens) - 1
                        else:
                            tokens.append(tk)
                            segments.append(1)

                    ids = tokenization.convert_tokens_to_ids(tokens=tokens, vocab=vocab)
                    length = len(ids)
                    if length > max_length:
                        length = max_length
                    for j in range(length):
                        sequence_has_ans[count, j] = ids[j]
                        segments_has_ans[count, j] = segments[j]
                        mask_has_ans[count, j] = 1
                    count += 1
                    #####################

sequence_has_ans_ = np.zeros(shape=[count, max_length], dtype=np.int32)
segments_has_ans_ = np.zeros(shape=[count, max_length], dtype=np.int32)
mask_has_ans_ = np.zeros(shape=[count, max_length], dtype=np.int32)
answer_span_ = np.zeros(shape=[count, 2], dtype=np.int32)
paragraph_type_ = np.zeros(shape=[count], dtype=np.int32)

sequence_has_ans_z_ = np.zeros(shape=[count, 3, max_length], dtype=np.int32)
segments_has_ans_z_ = np.zeros(shape=[count, 3, max_length], dtype=np.int32)
mask_has_ans_z_ = np.zeros(shape=[count, 3, max_length], dtype=np.int32)

for i in range(count):
    sequence_has_ans_[i] = sequence_has_ans[i]
    segments_has_ans_[i] = segments_has_ans[i]
    mask_has_ans_[i] = mask_has_ans[i]
    answer_span_[i] = answer_span[i]
    paragraph_type_[i] = paragraph_type[i]

    sequence_has_ans_z_[i] = sequence_has_ans_z[i]
    segments_has_ans_z_[i] = segments_has_ans_z[i]
    mask_has_ans_z_[i] = mask_has_ans_z[i]

np.save('sequence_table_z', sequence_has_ans_z_)
np.save('segments_table_z', segments_has_ans_z_)
np.save('mask_table_z', mask_has_ans_z_)

np.save('sequence_table', sequence_has_ans_)
np.save('segments_table', segments_has_ans_)
np.save('mask_table', mask_has_ans_)
np.save('answer_span_table', answer_span_)
np.save('paragraph_type_table', paragraph_type_)

