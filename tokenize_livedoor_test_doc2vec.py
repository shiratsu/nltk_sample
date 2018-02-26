# -*- coding: utf-8 -*-
#
# tokenizeの実験
#
import MeCab
from gensim import corpora
import glob
import sys
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import LabeledSentence

training_docs = []
mecab = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
mecab.parse('')

def makeData(strDir):
    dirlist = glob.glob(strDir+'/*')
    dicSentence = {}

    #print(dirlist)

    for d in dirlist:

        if d == 'README.txt' or d == '.DS_Store':
            continue

        #print(d)

        filelist = glob.glob(d+'/*')

        for strfile in filelist:
            arySentence = []
            dicSentence[strfile] = ''

            #print(strfile)

            with open(strfile,'r') as f:

                flines = f.readlines()
            
                for line in flines:
                    arySentence.append(line)

            dicSentence[strfile] = ''.join(arySentence)
            

    return dicSentence

def tokenize(text):
    '''
    とりあえず形態素解析して名詞だけ取り出す感じにしてる
    '''
    node = mecab.parseToNode(text)
    while node:
        if node.feature.split(',')[0] == '名詞':
            yield node.surface.lower()
        node = node.next


def get_words(contents):
    '''
    記事群のdictについて、形態素解析してリストにして返す
    '''
    ret = []
    dicCorpus = {}
    for k, content in contents.items():
        #ret.append(get_words_main(content))
        dicCorpus[k] = get_words_main(content)
    return dicCorpus


def get_words_main(content):
    '''
    一つの記事を形態素解析して返す
    '''
    return [token for token in tokenize(content)]

# 2記事の一部だけ取り出しました
# 1つめがITライフハック、2つめが独女通信の記事です。
if __name__ == '__main__':

    args = sys.argv

    dicSentence = makeData('livedoor')

    dicCorpus = get_words(dicSentence)
    
    training_docs = []
    for k,v in dicCorpus.items():
        training_docs.append(LabeledSentence(words=v, tags=[k]))

    model = Doc2Vec(documents=training_docs, size=100 , window=3, min_count=15, dm=1)

    model.save('livedoor_doc2vec.model')
    
