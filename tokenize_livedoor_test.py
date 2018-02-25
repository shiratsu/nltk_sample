# -*- coding: utf-8 -*-
#
# tokenizeの実験
#
import MeCab
from gensim import corpora
import glob

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

        dicSentence[d] = ''
        arySentence = []
        filelist = glob.glob(d+'/*')

        for strfile in filelist:

            #print(strfile)

            with open(strfile,'r') as f:

                flines = f.readlines()
            
                for line in flines:
                    arySentence.append(line)

            
        dicSentence[d] = ''.join(arySentence)

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

    dicSentence = makeData('livedoor')

    #words = get_words({'it-life-hack-001.txt': 'アナタはまだブラウザのブックマーク？　ブックマーク管理はライフリストがオススメ 最近ネットサーフィンをする際にもっぱら利用しているのが「ライフリスト」というサイトだ。この「ライフリスト」は、ひとことで言うと自分専用のブックマークサイトである。というよりブラウザのスタートページにするとブラウザのブックマーク管理が不要になる便利なサイトなのである。', 'dokujo-tsushin-001.txt': 'たとえば、馴れ馴れしく近づいてくるチャラ男、クールを装って迫ってくるエロエロ既婚男性etc…に対し「下心、見え見え〜」と思ったことはないだろうか？ “下心”と一言で言うと、特に男性が女性のからだを目的に執拗に口説くなど、イヤらしい言葉に聞こえてしまう。実際、辞書で「下心」の意味を調べてみると、心の底で考えていること。かねて心に期すること、かねてのたくらみ。特に、わるだくみ。（広辞苑より）という意味があるのだから仕方がないのかもしれない。'})
    words = get_words(dicSentence)

    #print(words)

    dictionary = corpora.Dictionary(words)
    # no_berow: 使われてる文章がno_berow個以下の単語無視
    # no_above: 使われてる文章の割合がno_above以上の場合無視
    #dictionary.filter_extremes(no_below=20, no_above=0.3)    
    dictionary.filter_extremes(no_below=5,no_above=0.7)    
    print("-------------------token後-------------------")
    print(dictionary.token2id)
    dictionary.save_as_text('livedoor_test1.dict')


    
