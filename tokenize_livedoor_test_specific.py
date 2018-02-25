# -*- coding: utf-8 -*-
#
# tokenizeの実験
#
import MeCab
from gensim import corpora
import glob
import sys

mecab = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
mecab.parse('')

def makeData(strDir,strSpecific):
    filelist = glob.glob(strDir+'/'+strSpecific+'/*')
    dicSentence = {}

    #print(dirlist)
    for strfile in filelist:
        arySentence = []
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
    for k, content in contents.items():
        ret.append(get_words_main(content))
    return ret


def get_words_main(content):
    '''
    一つの記事を形態素解析して返す
    '''
    return [token for token in tokenize(content)]

# 2記事の一部だけ取り出しました
# 1つめがITライフハック、2つめが独女通信の記事です。
if __name__ == '__main__':

    args = sys.argv

    dicSentence = makeData('livedoor',args[1])

    words = get_words(dicSentence)

    #print(words)

    dictionary = corpora.Dictionary(words)
    print("-------------------token前-------------------")
    print(dictionary.token2id)
    print(len(dictionary))
    dictionary.save_as_text(args[1]+'_nofilter.dict')
    # no_berow: 使われてる文章がno_berow個以下の単語無視
    # no_above: 使われてる文章の割合がno_above以上の場合無視
    dictionary.filter_extremes(no_below=15, no_above=0.3)    
    #dictionary.filter_extremes(no_below=1)    
    print("-------------------token後-------------------")
    print(dictionary.token2id)
    print(len(dictionary))
    dictionary.save_as_text(args[1]+'.dict')


    
