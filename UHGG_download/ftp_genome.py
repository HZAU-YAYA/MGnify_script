#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import logging
import argparse
import sys

LOG = logging.getLogger(__name__)
__version__ = "1.0.0"  # 设置版本信息
__author__ = ("Boya Xu",)  # 输入作者信息
__email__ = "834786312@qq.com"
__all__ = []


def add_help_args(parser):  # 帮助函数
    parser.add_argument('--input_file', type=str, default=False, help="输入文件")
    parser.add_argument('--rank_line', type=str, default=False, help="输出物种，rank level__name")
    return parser


def read_file(input_file, rank_line):
    data = {}
    rank = rank_line.split('__')[0]
    level_name = rank_line.split('__')[1]
    with open(input_file, 'r') as f:
        next(f)
        for line in f:
            if line.startswith('#'):
                continue
            l = line.strip().split('\t')
            Taxonomy_lineage = l[14]
            if rank == 'p':
                taxon = re.search(r'p__([^;]+)', Taxonomy_lineage)
                if taxon:
                    taxon = taxon.group(1)
                    if taxon == level_name:
                        data[l[0]] = [Taxonomy_lineage, l[-1]]
                else:
                    print(f'warning: {Taxonomy_lineage} no p__ in Taxonomy_lineage')

            elif rank == 'c':
                taxon = re.search(r'c__([^;]+)', Taxonomy_lineage)
                if taxon:
                    taxon_name = taxon.group(1)
                    if taxon_name == level_name:
                        data[l[0]] = [Taxonomy_lineage, l[-1]]
                else:
                    print(f'warning: {Taxonomy_lineage} no c__ in Taxonomy_lineage')
            elif rank == 'o':
                taxon = re.search(r'o__([^;]+)', Taxonomy_lineage)
                if taxon:
                    taxon_name = taxon.group(1)
                    if taxon_name == level_name:
                        data[l[0]] = [Taxonomy_lineage, l[-1]]
                else:
                    print(f'warning: {Taxonomy_lineage} no o__ in Taxonomy_lineage')
            elif rank == 'f':
                taxon = re.search(r'f__([^;]+)', Taxonomy_lineage)
                if taxon:
                    taxon_name = taxon.group(1)
                    if taxon_name == level_name:
                        data[l[0]] = [Taxonomy_lineage, l[-1]]
                else:
                    print(f'warning: {Taxonomy_lineage} no f__ in Taxonomy_lineage')
            elif rank == 'g':
                taxon = re.search(r'g__([^;]+)', Taxonomy_lineage)
                if taxon:
                    taxon_name = taxon.group(1)
                    if taxon_name == level_name:
                        data[l[0]] = [Taxonomy_lineage, l[-1]]
                else:
                    print(f'warning: {Taxonomy_lineage} no g__ in Taxonomy_lineage')
            elif rank == 's':
                taxon = re.search(r's__([^;]+)', Taxonomy_lineage)
                if taxon:
                    taxon_name = taxon.group(1)
                    if taxon_name == level_name:
                        data[l[0]] = [Taxonomy_lineage, l[-1]]
                else:
                    print(f'warning: {Taxonomy_lineage} no s__ in Taxonomy_lineage')
    with open('id_taxonmy_ftp.txt', 'w') as f:
        for k, v in data.items():
            f.write(f'{k}\t{v[0]}\t{v[1]}\n')

def main():  # 主函数，执行函数
    logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="[%(levelname)s] %(message)s")
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=''' 
name:statistic.py 
attention: 全contig画图
version: %s
contact: %s <%s>\ 
''' % (__version__, ' '.join(__author__), __email__))
    args = add_help_args(parser).parse_args()
    read_file(args.input_file, args.rank_line)


if __name__ == "__main__":  # 固定格式，使 import 到其他的 python 脚本中被调用（模块重用）执行
    main()
