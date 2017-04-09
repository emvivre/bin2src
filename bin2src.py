#!/usr/bin/python
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

def output_c_cpp(o_fd, input_file, variable_name_source):
    o_fd.write(
'''
const unsigned char %s[] = {
''' % variable_name_source)
    l = 0        
    f = open(input_file)
    while True:
        data = f.read(16)
        if len(data) == 0:
            break
        l += len(data)
        o_fd.write('    ')
        for d in data:
            o_fd.write('0x%02X,' % ord(d))
        o_fd.write('\n')
    o_fd.write(
'''};

const unsigned int %s_sz = %s;
''' % (variable_name_source, l))
    
def output_assembler(o_fd, input_file, variable_name_source):
    l = os.path.getsize(input_file)
    input_file = os.path.basename(input_file)
    o_fd.write(
'''
    .global %s
    .global %s_sz
%s:
    .incbin "%s"
%s_sz:
    .int %d
''' % (variable_name_source, variable_name_source, variable_name_source, input_file, variable_name_source, l))
    
if len(sys.argv) < 4:
    print 'Usage: %s <INPUT_FILE_0> [<INPUT_FILE_1> ...] <OUTPUT_SOURCE> <OUTPUT_HEADER>' % sys.argv[0]
    print '   ex: %s /etc/passwd coco.cpp coco.h' % sys.argv[0]
    print '   ex: %s /etc/passwd coco.S coco.h' % sys.argv[0]
    quit(1)

input_files = sys.argv[1:-2]
(output_source, output_header) = sys.argv[-2:]
variable_name = output_header.split('.')[0].replace('+', '_').replace('-', '_')
variables = []

is_assembler = output_source.endswith('.s') or output_source.endswith('.S')

o_fd = open(output_source, 'w+')
if is_assembler is False:
    o_fd.write(
        '''#include "%s"
        ''' % output_header)
for input_file in input_files:
    if len(input_files) == 1:
        variable_name_source = variable_name
    else:
        variable_name_source = '%s_%s' % (variable_name, os.path.basename(input_file).replace('+', '_').replace('-', '_').replace('.', '_'))
        
    if variable_name_source in variables:
        print 'ERROR: collision of variable name "%s" !!!!' % variable_name_source
        quit(1)
    variables.append( variable_name_source )

    if is_assembler is True:
        output_assembler(o_fd, input_file, variable_name_source)
    else:
        output_c_cpp(o_fd, input_file, variable_name_source)
    
o_fd = open(output_header, 'w+')
define_name = output_header.replace('.', '_').upper()
o_fd.write(
'''#ifndef _%s_
#define _%s_
''' % (define_name, define_name))
for v in variables:
    o_fd.write(
'''
extern const unsigned char %s[];
extern const unsigned int %s_sz;
''' % (v, v))
o_fd.write(
'''
#endif
''')
    
