#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import argparse
import sys
import concurrent.futures

LOG = logging.getLogger(__name__)
__version__ = "1.0.1"  # 更新版本信息
__author__ = ("Boya Xu",)  # 作者信息
__email__ = "834786312@qq.com"
__all__ = []


def add_help_args(parser):  # 帮助函数
    parser.add_argument('--path', metavar='PATH', type=str, help="下载文件的路径")
    parser.add_argument('--input', metavar='INPUT', type=str, help="输入文件名")
    parser.add_argument('--threads', metavar='THREADS', type=int, default=8, help="线程数，默认为8")
    return parser


def download_file(url, folder_name, file_name):
    lock_filename = folder_name + file_name + '.lock'  # 定义锁文件名
    with open(lock_filename, 'w') as lockfile:
        try:
            os.system(f"wget -O {folder_name}{file_name} {url}")
            # 下载文件的代码...
        except Exception as e:
            LOG.error(f"Error downloading file: {e}")
        finally:
            os.remove(lock_filename)


def wget_genomes(file, path, thread_num=8):
    data_MAG = {}
    data_Isolate = {}
    with open(file, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith('#'):
            continue
        genome_accession, g_type, taxon, url = line.split('\t')
        if g_type == 'MAG':
            data_MAG[genome_accession] = url
        elif g_type == 'Isolate':
            data_Isolate[genome_accession] = url
        else:
            LOG.warning(f'警告：类型 {g_type} 不存在。')
    MAG_path = os.path.join(path, 'MAG/')
    Isolate_path = os.path.join(path, 'Isolate/')
    os.makedirs(MAG_path, exist_ok=True)
    os.makedirs(Isolate_path, exist_ok=True)
    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_num) as executor:
        for genome_accession, url in data_MAG.items():
            LOG.info('Downloading ' + genome_accession + '.fna ...')
            futures.append(executor.submit(download_file, url, MAG_path, genome_accession + '.fna'))
        for genome_accession, url in data_Isolate.items():
            LOG.info('Downloading ' + genome_accession + '.fna ...')
            futures.append(executor.submit(download_file, url, Isolate_path, genome_accession + '.fna'))
        concurrent.futures.wait(futures)
    LOG.info('所有下载已完成。')


def main():  # 主函数，执行函数
    logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="[%(levelname)s] %(message)s")
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=f''' 
name: download_refseq.py 
attention: python download_MGnify.py --input <file> --path <path> --threads <num>
version: {__version__}
contact: {' '.join(__author__)} <{__email__}> 
''')
    args = add_help_args(parser).parse_args()
    wget_genomes(args.input, args.path, args.threads)


if __name__ == "__main__":  # 固定格式，使 import 到其他的 python 脚本中被调用（模块重用）执行
    main()
