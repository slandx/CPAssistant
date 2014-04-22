#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-04-18 13:17:25
# @Author  : Ho1iarty (ho1iarty@gmail.com)
# @Version : 0.1

import os
import jieba
from argparse import ArgumentParser
import sqlite3 as lite
import logging

logging.basicConfig(filename = os.path.join(os.getcwd(), 'cpassistant.log'),
    level = logging.DEBUG, filemode = 'a', 
    format = '%(asctime)s - %(levelname)s: %(message)s')

def contains_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
        return False

def output(zi_list, yin_list):
    out_zi_list = []
    out_yin_list = []
    output_list = []
    for (idx,yin) in enumerate(yin_list):
        if contains_chinese(zi_list[idx]):
            for (idx_y,each_y) in enumerate(yin.split()):
                out_yin_list.append('['+each_y+']')
                out_zi_list.append(' '*(len(each_y)/2)+zi_list[idx][idx_y]+' '*(len(each_y)-len(each_y)/2))
        else:
            out_yin_list.append(yin)
            out_zi_list.append(zi_list[idx])
            if '\n' in yin:
                output_list.append(''.join(out_yin_list))
                output_list.append(''.join(out_zi_list))
                del out_zi_list[:]
                del out_yin_list[:]
    # end for
    if len(out_zi_list):
        out_yin_list.append('\n')
        out_zi_list.append('\n')
        output_list.append(''.join(out_yin_list))
        output_list.append(''.join(out_zi_list))
    print ''.join(output_list)


def get_jyutping(cur,phrase):
    # Exact Match
    cur.execute("select YIN from DICT_CI where JIAN='"+phrase+"';")
    rst = cur.fetchone()
    if rst:
        return rst[0]
    else:
        # Matching separately
        logging.info("No result in DICT_CI: %s" % phrase)
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
    # get db connection
    con = None
    try:
        result = list(jieba.cut(sentence))
        con = lite.connect('jyut_zh.dict')
        cur = con.cursor()
        zi_list = []
        yin_list = []
        for phrase in result:
            zi_list.append(phrase)
            if contains_chinese(phrase):
                jyutp = get_jyutping(cur, phrase)
                yin_list.append(jyutp)
                # print phrase.encode('utf-8'), jyutp.encode('utf-8')
            else:
                yin_list.append(phrase)
        # end for
        output(zi_list,yin_list)
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
            parser.print_help()

if __name__ == "__main__":
    main()
    

