'''
Created on Mar 20, 2014

@author: dgrewal
'''

import argparse

chrom_list = map(str, range(1, 23)) + ['X', 'Y']

parser = argparse.ArgumentParser()

parser.add_argument('--input',  
                    required=True, 
                    help='the input bam file')

parser.add_argument('--output',  
                    required=True, 
                    help='the output bam file')

parser.add_argument('--prefix', 
                    required = True,
                    help='The prefix string that will be added')

args,unknown = parser.parse_known_args()
