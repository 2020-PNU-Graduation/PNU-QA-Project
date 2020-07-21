from eunjeon import Mecab
# https://github.com/koshort/pyeunjeon
class Chuncker:
    def __init__(self):

        self.tagger =  Mecab()
        self.Bi_charcter_feature = []

    def get_feautre(self, query):
        self.Bi_charcter_feature = []

        TKs = self.tagger.morphs(query)

        for TK in TKs:
            if len(TK) > 1:
                for i in range(1, len(TK)):
                    self.Bi_charcter_feature.append(str(TK[i - 1: i + 1]))

        #print(self.Bi_charcter_feature)

    def get_chunk_score(self, paragraph):
        score = 0

        for ch_feat in self.Bi_charcter_feature:
            if paragraph.find(ch_feat) != -1:
                score += 1

        return 1 + score / len(self.Bi_charcter_feature)