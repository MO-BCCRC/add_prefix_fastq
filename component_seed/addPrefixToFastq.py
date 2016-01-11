#!/share/lustre/csiu/apps/python2.7/bin/python2.7
# Author:  Celia Siu
# Created: 2014-08-28
import argparse
import os
import gzip

import re
usage = """
"""
version = '1.0.1'

def is_gzip(filename):
    if filename.split('.')[-1] == 'gz':
        return True
    return False

def main(fastqfile, prefix, outfile):
    if not os.path.isfile(fastqfile):
        raise Exception('cannot find %s' % fastqfile)

    if outfile == None:
        outfile = '%s.prefixed.fq' % fastqfile

    read_count = 1
    line_count = 0
    
    if is_gzip(fastqfile):
        f = gzip.open(fastqfile, 'rb')
    else:
        f = open(fastqfile, 'r')
    with open(outfile, 'w') as out:
        for line in f:
            if line.startswith('@') and line_count % 4 == 0:
                 out.write(re.sub('^@', '@%s_%d:' % (prefix, read_count), line))
                 read_count += 1
                 line_count += 1	    
            else:
                 out.write(line)
                 line_count += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=usage, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--infile', dest='infile',
                        required=True,
                        help='path to fastq file')
    
    parser.add_argument('-o', '--outfile', dest='outfile',
                        help='specify path to fastq file after prefix')
    
    parser.add_argument('-p', '--prefix', dest='prefix',
                        default='read',
                        help='string to be appended to each sequence identifier of fastq')
    
    ##et at the arguments
    args = parser.parse_args()
    
    ## do something..
    main(args.infile, args.prefix, args.outfile)
