'''
File Splitter App (command line version)

This app takes in a source file, and splits it into two separate files, with
odd lines in the first target file, and even lines in the second target file.

It was developed to help split a single-file corpus containing language-pair
lines, with source language text in one line, and the target language text
in the next line. This app will split the corpus into two files, one containing
the source language text, and the other containing the target language text.

Usage:
    python filesplitter_cmdline.py <source_file> <target1_file> <target2_file>
    
    where:
        source_file:    File to split, containing source language text in one
                        line, and target language text in another line.
        target1_file:   Name of file to output source language text to.
        target2_file:   Name of file to output target language text to.

Created on Feb 15, 2017
Feb 19, 2017:    Implemented command line argument handling with argparse.

@author: vivian
'''
from __future__ import print_function
import argparse


def split_file(source_filename, target1_filename, target2_filename, open_flag):
    """ Method to handle actual logic for the app.
        Read in lines from source file, then save odd lines in one file,
        and even lines in another file.
        
        Note: In Python, although line numbering will start with 0, 1, 2,...
        the source file is being split according to normal human convention
        for odd and even line numbering, i.e. the first line in the source
        file will be stored in the array "odd_lines" while the second line
        will be stored in "even_lines".
    """
    with open(source_filename) as stream_in:
        lines = stream_in.readlines()
    odd_lines, even_lines = lines[::2], lines[1::2]
    with open(target1_filename, open_flag) as stream_out1:
        for odd_line in odd_lines:
            stream_out1.write(odd_line)
    with open(target2_filename, open_flag) as stream_out2:
        for even_line in even_lines:
            stream_out2.write(even_line)            
    print("File split completed!")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file")
    parser.add_argument("target_file1")
    parser.add_argument("target_file2")
    parser.add_argument("-a", "--append", help="append to existing file",
                        action="store_true")
    args = parser.parse_args()
    if args.append:
        open_flag = "a"
    else:
        open_flag = "w"
        
    split_file(args.source_file, args.target_file1, args.target_file2, open_flag)

    
if __name__ == "__main__":
    main()
