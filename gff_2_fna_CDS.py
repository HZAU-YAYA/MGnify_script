#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import logging
import argparse
import sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqFeature import SeqFeature, FeatureLocation
from Bio.Data import CodonTable

LOG = logging.getLogger(__name__)
__version__ = "1.0.0"  # 设置版本信息
__author__ = ("Boya Xu",)  # 输入作者信息
__email__ = "834786312@qq.com"
__all__ = []


def add_help_args(parser):  # 帮助函数
    parser.add_argument('--gcf', type=str, default=False, help="输出文件前缀")
    parser.add_argument('--gff', type=str, default=False, help="输入gff文件")
    parser.add_argument('--en', action='store_true', help="是否保留终止密码子符号, True/False")
    return parser


def read_file(gff, gcf, en):
    data_CDS = {}

    with open(gff, 'r') as f1, open(gcf+'.genomic.fna', 'w') as f2:
        start_genome = 'N'
        for line in f1:
            if line.startswith('##gff-version') or line.startswith('##sequence-region'):
                continue
            if line.startswith('##FASTA'):
                start_genome = 'Y'
                continue
            if start_genome == 'N':
                l = line.strip().split('\t')
                if l[2] == 'CDS':
                    if l[0] not in data_CDS:
                        data_CDS[l[0]] = {}
                    gene_ID = re.search(r'ID=([^;]*)(;|$)', l[8]).group(1)
                    product = re.search(r'product=([^;]*)(;|$)', l[8]).group(1)
                    data_CDS[l[0]][gene_ID] = [l[3], l[4], l[6], product]
            elif start_genome == 'Y':
                f2.write(line)
    with open(gcf+'.pro.fa', 'w') as f1, open(gcf+ '.nucl.fa', 'w') as f2:
        for record in SeqIO.parse(gcf+'.genomic.fna', 'fasta'):
            if record.id in data_CDS:
                for gene_ID in data_CDS[record.id]:
                    start, end, strand, product = data_CDS[record.id][gene_ID]
                    start = int(start)
                    end = int(end)
                    if strand == '+':
                        seq = record.seq[start-1:end]
                        pro_seq = seq.translate(table=11)
                        if en:
                            pro_seq = pro_seq.replace('*', '')
                    else:
                        seq = record.seq[start-1:end].reverse_complement()
                        pro_seq = seq.translate(table=11)
                        if en:
                            pro_seq = pro_seq.replace('*', '')
                    f1.write('>' + gene_ID + ' ' + product + '\n' + str(pro_seq) + '\n')
                    f2.write('>' + gene_ID + ' ' + product + '\n' + str(seq) + '\n')



def main():  # 主函数，执行函数
    logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="[%(levelname)s] %(message)s")
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=''' 
name:statistic.py 
attention: 使用biopython将特定gff转换为CDS序列，并提取里面的基因组片段
version: %s
contact: %s <%s>\ 
''' % (__version__, ' '.join(__author__), __email__))
    args = add_help_args(parser).parse_args()
    read_file(args.gff, args.gcf, args.en)


if __name__ == "__main__":  # 固定格式，使 import 到其他的 python 脚本中被调用（模块重用）执行
    main()
