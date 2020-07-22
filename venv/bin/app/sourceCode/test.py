from eunjeon import Mecab


tagger = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')

sentence = '아무문장이다.'
# print(tagger.morphs(sentence))

#아나콘다 환경
#python 3.6
#대소 비교가 가능한 숫자(뭐 ~km) 같은거 2차언 배열로 순위 매기기
#대소 비교 불가능한 건 0 으로 처리하고 1순위부터 시작해서 2차원 배열 생성

# '/usr/local/lib/mecab/dic/mecab-ko-dic'