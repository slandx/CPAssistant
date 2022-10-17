#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-04-18 13:17:25
# @Author  : Ho1iarty (ho1iarty@gmail.com)
# @Version : 0.1

from operator import le
import os
import jieba
from argparse import ArgumentParser
import sqlite3 as lite
import logging
import chardet

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('youyuan', 'youyuan.ttf'))

jieba.setLogLevel(logging.INFO)

logging.basicConfig(filename=os.path.join(os.getcwd(), 'cpassistant.log'),
                    level=logging.DEBUG, filemode='a',
                    format='%(asctime)s - %(levelname)s: %(message)s')


def contains_chinese(check_str):
    for ch in check_str:
        if '\u4e00' <= ch <= '\u9fff':
            return True
        return False


def generate_pdf_file(pdf_name, lines):
    doc = SimpleDocTemplate(
        pdf_name,
        pagesize=defaultPageSize,
        bottomMargin=.4 * inch,
        topMargin=.4 * inch,
        rightMargin=.8 * inch,
        leftMargin=.8 * inch)
    style = ParagraphStyle(
        name='Normal',
        fontName='youyuan',
        fontSize=9,
    )
    story = []
    for value in lines:
        P = Paragraph(value, style)
        story.append(P)

    doc.build(
        story,
    )

def output(zi_list, yin_list, pdf_file_name):
    out_zi_list = []
    out_yin_list = []
    output_list = []
    for (idx, yin) in enumerate(yin_list):
        if contains_chinese(zi_list[idx]):
            for (idx_y, each_y) in enumerate(yin.split()):
                out_yin_list.append('['+each_y+']')
                out_zi_list.append(' '*int(len(each_y)/2)+zi_list[idx][idx_y]+' '*(len(each_y)-int(len(each_y)/2)))
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
    if len(pdf_file_name):
        generate_pdf_file(pdf_file_name, [x.replace(" ","&nbsp;") for x in output_list])
    else:
        print(''.join(output_list))


def get_jyutping(cur, phrase):
    # Exact Match
    cur.execute("select YIN from DICT_CI where JIAN='"+phrase+"';")
    rst = cur.fetchone()
    if rst:
        return rst[0]
    else:
        # Matching separately
        logging.info("No result in DICT_CI: %s" % phrase)
        if len(phrase) == 1:
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


def mark_sentence(sentence, pdf_file_name):
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
        output(zi_list, yin_list, pdf_file_name)
    except Exception as e:
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
    parser.add_argument('-p', '--pdf', help='output to PDF file', type=str)
    return parser


def main():
    parser = get_parser()
    options = parser.parse_args()
    if options:
        if options.file:
            # use file
            fileObj = None
            try:
                fileObj = open(options.file, 'rb')
                f_content = fileObj.read()
                enc_rst = chardet.detect(f_content)
                mark_sentence(f_content.decode(enc_rst['encoding']), options.pdf)
            except Exception as e:
                print(e)
            finally:
                if fileObj:
                    fileObj.close()
        elif options.str:
            mark_sentence(options.str, options.pdf)
        else:
            parser.print_help()


if __name__ == "__main__":
    main()
