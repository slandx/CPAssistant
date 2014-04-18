#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-04-18 13:17:25
# @Author  : Ho1iarty (ho1iarty@gmail.com)
# @Version : 0.1

import jieba
from argparse import ArgumentParser
import sqlite3 as lite

def get_jyutping(cur,phrase):
    # 1. Exact Match
    cur.execute("select YIN from DICT_CI where JIAN='"+phrase+"';")
    rst = cur.fetchone()
    if rst:
        return rst[0]
    else:
        # 2. Fuzzy Match
        cur.execute("select YIN from DICT_CI where JIAN like '%"+phrase+"%';")
        rst = cur.fetchone()
        if rst:
            return rst[0]
        else:
            # 3. Matching separately
            if len(phrase)==1:
                cur.execute("select YIN from DICT_ZI where ZI='"+phrase+"';")
                rst = cur.fetchone()
                if rst:
                    return rst[0].split()[0]
                else:
                    return '  '
            else:
                tmp = []
                for word in phrase:
                    tmp.append(get_jyutping(cur, word))
                return ' '.join(tmp)

def mark_sentence(sentence):
    result = list(jieba.cut(sentence))
    # result = [u'这是',u'一个',u'伸手不见五指',u'里',u'黑夜']
    # get db connection
    con = None
    try:
        con = lite.connect('jyut_zh.dict')
        cur = con.cursor()
        for phrase in result:
            jyutp = get_jyutping(cur, phrase)
            print phrase.encode('utf-8'), jyutp.encode('utf-8')
    except Exception, e:
        raise e
    finally:
        if con:
            con.close()
        

def get_parser():
    parser = ArgumentParser(description='Convert Chinese to Cantonese.')
    parser.add_argument('-v', '--version', action='version',
                        version='{0} {1}'.format('CP Assistant', '0.1 Beta'))
    parser.add_argument('-f', '--file', help='file path', type=str)
    parser.add_argument('-s', '--str', help='chinese string', type=str)
    return parser

def main():
    parser = get_parser()
    options = parser.parse_args()
    if options:
        if options.file:
            # use file
            fileObj = None
            try:
                fileObj = open(options.file,'r')
                mark_sentence(fileObj.read().decode('utf-8'))
            except Exception, e:
                print e
            finally:
                if fileObj:
                    fileObj.close()
        elif options.str:
            # use string
            mark_sentence(options.str.decode('utf-8'))
        else:
            print "Error!"

if __name__ == "__main__":
    mark_sentence("归家谁有几里路谁能预算")
    # main()
    

