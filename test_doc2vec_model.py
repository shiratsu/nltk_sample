# -*- coding: utf-8 -*-
#
# doc2vecモデルのテスト
#
from gensim.models.doc2vec import Doc2Vec
import sys

args = sys.argv

model = Doc2Vec.load('livedoor_doc2vec.model')

# 文章を指定してそれに近い文章を抽出する

result = model.docvecs.most_similar('livedoor/'+args[1]+'/'+args[2], topn=1)

print(result)
