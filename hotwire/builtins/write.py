# This file is part of the Hotwire Shell project API.

# Copyright (C) 2007 Colin Walters <walters@verbum.org>

# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
# of the Software, and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE 
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR 
# THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os,sys,pickle

import hotwire
from hotwire.builtin import Builtin, BuiltinRegistry, InputStreamSchema, MultiArgSpec
from hotwire.fs import FilePath, open_text_file
from hotwire.sysdep.fs import Filesystem

class WriteBuiltin(Builtin):
    __doc__ = _("""Save stream to files.""")
    def __init__(self):
        super(WriteBuiltin, self).__init__('write',
                                           input=InputStreamSchema('any', optional=False),
                                           argspec=MultiArgSpec('paths', min=1),
                                           options=[['-a', '--append'],['-p', '--pickle'],
                                                    ['-n', '--newline']])

    def execute(self, context, args, options=[]):
        open_mode = ('-a' in options) and 'a+' or 'w'
        do_pickle = '-p' in options
        with_newline = '-n' in options
        if do_pickle:
            open_mode = 'wb'
        if not context.input:
            return
        streams = [open_text_file(FilePath(x, context.cwd), open_mode) for x in args]
        if not do_pickle:
            for arg in context.input:
                for stream in streams:
                    stream.write('%s' % (str(arg),))
                    if with_newline:
                        stream.write('\n')
        else:
            # Kind of annoying pickle makes you do this.
            arglist = list(context.input)
            for stream in streams:
                pickle.dump(arglist, stream)
        list(map(lambda x: x.close(), streams))
        return []

BuiltinRegistry.getInstance().register_hotwire(WriteBuiltin())
