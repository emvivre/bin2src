#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

"""
  ===========================================================================

  Copyright (C) 2013 Emvivre

  This file is part of BIN2HEADER.

  BIN2HEADER is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  BIN2HEADER is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with BIN2HEADER.  If not, see <http://www.gnu.org/licenses/>.

  ===========================================================================
*/
"""

import sys
import os

def generate_variable_name_from_source( source ):
    return source.split('.')[0].replace('+', '_').replace('-', '_')

def generate_hex_array( input_file, space=4 ):
    s = ''
    l = 0
    f = open(input_file, 'rb')
    while True:
        data = f.read(16)
        if len(data) == 0:
            break
        l += len(data)
        s += ' ' * space
        for d in data:
            s += '0x%02X,' % d
        s += '\n'
    f.close()
    return (s,l)

def output_c_cpp(input_file, variable_name_source, output_header):
    s = ''
    if len(output_header):
        s += '''#include "%s"

''' % output_header
    s += '''const unsigned char %s[] = {
''' % variable_name_source
    (ss, l) = generate_hex_array( input_file )
    s += ss
    s += '''};

const unsigned int %s_sz = %s;
''' % (variable_name_source, l)
    return s

def output_cs(input_file, variable_name_source):
    class_name = variable_name_source[0].upper() + variable_name_source[1:]
    s = '''namespace Project
{
    static class %s
    {
        public static byte[] %s = {
''' % (class_name, variable_name_source)
    (ss, l) = generate_hex_array( input_file, 4*3 )
    s += ss
    s += '''        };
    }
}'''
    return s

def output_assembler(input_file, variable_name_source):
    l = os.path.getsize(input_file)
    input_file = os.path.basename(input_file)
    s = '''
    .global %s
    .global %s_sz
%s:
    .incbin "%s"
%s_sz:
    .int %d
''' % (variable_name_source, variable_name_source, variable_name_source, input_file, variable_name_source, l)
    return s

if len(sys.argv) < 3:
    print('''Usage: %(arg0)s <INPUT_FILE> <OUTPUT_SOURCE> [<OUTPUT_HEADER>]
with <OUTPUT_SOURCE> : *.s / *.S / *.c / *.cpp / *.cs
  ex: %(arg0)s /etc/passwd coco.cpp coco.h
  ex: %(arg0)s /etc/passwd coco.S coco.h''' % {'arg0': sys.argv[0]})
    quit(1)

(input_file, output_source) = sys.argv[1:3]
output_header = sys.argv[-1] if len(sys.argv) > 3 else ''
source_ext = output_source.split('.')[-1]
variable_name = generate_variable_name_from_source( output_source )

## export source
if source_ext in ['s', 'S']:
    s = output_assembler( input_file, variable_name )
elif source_ext in ['c', 'cpp']:
    s = output_c_cpp( input_file, variable_name, output_header )
elif source_ext == 'cs':
    s = output_cs( input_file, variable_name )
else:
    print('ERROR: invalid output format given !')
    quit(1)

with open(output_source, 'w+b') as o_fd:
    o_fd.write( bytes(s,'utf-8') )

## export header
if len(output_header) > 0:
    s = ''
    define_name = output_header.replace('.', '_').upper()
    s += '''#ifndef _%s_
#define _%s_
''' % (define_name, define_name)
    s += '''
extern const unsigned char %s[];
extern const unsigned int %s_sz;
''' % (variable_name, variable_name)
    s += '''
#endif
'''
    with open(output_header, 'w+b') as o_fd:
        o_fd.write( bytes(s,'utf-8') )
