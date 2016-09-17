#!/usr/bin/env python
# encoding: utf-8

# Copyright (c) 2016, Florian Brucker (www.florianbrucker.de)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
A logging handler that forwards log messages to IFTTT.com.

IFTTT.com is a platform that allows you to setup automatic reactions to
a wide range of events. This module provides a logging handler that
forwards log messages to IFTTT so that you can automatically react to
them (for example to get an e-mail if that cron job on some remote
server you keep forgetting about logs an error).
'''

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
import logging.handlers
import sys
import traceback

import requests


__version__ = '0.1.0'

if sys.version_info < (3,):
    str, bytes = unicode, str
    from urllib import quote
else:
    from urllib.parse import quote


class IFTTTLoggingHandler(logging.Handler):
    '''
    Logging handler that forwards log messages to IFTTT.com.
    '''

    _URL_TEMPLATE = 'https://maker.ifttt.com/trigger/{event}/with/key/{key}'

    def __init__(self, key, event, values=None, level=logging.NOTSET):
        '''
        Constructor.

        ``key`` and ``event`` are strings containing your secret IFTTT
        maker channel key and the IFTTT event name, respectively.

        ``values`` is an optional callback that receives a
        ``logging.LogRecord`` instance and returns up to 3 values which
        are converted to strings and passed to IFTTT. By default, the
        following values are passed: The formatted log message, the
        location where the message was logged (filename and line
        number), and, if available, the traceback embedded in the log
        record.

        ``level`` is the handler's logging level threshold. If not given
        then the handler accepts log messages of all levels (note that
        the logger to which the handler is attached may also have a
        level threshold).
        '''
        super(IFTTTLoggingHandler, self).__init__(level=level)
        self._url = self._URL_TEMPLATE.format(key=quote(key, ''),
                                              event=quote(event, ''))
        self._values = values

    def emit(self, record):
        values = self._record_to_values(record)
        if not isinstance(values, (list, tuple)):
            values = [values]
        values = [str(v) for v in values] + [''] * (3 - len(values))
        data = {'value1': values[0], 'value2': values[1], 'value3': values[2]}
        r = requests.post(self._url, json=data)
        r.raise_for_status()

    def _record_to_values(self, record):
        '''
        Generate values that are passed to IFTTT.

        IFTTT maker events accept up to 3 additional strings. This
        method receives a ``logging.LogRecord`` instance and returns
        the values to be sent.

        Within IFTTT, the values can then be used via the "ingredients"
        ``{{value1}}``, ``{{value2}}`` and ``{{value3}}``.

        The default implementation returns the formatted log message,
        the location where the warning was raised (filename and line
        number), and, if available, an exception traceback.

        A custom implementation in a subclass can return up to three
        values that are automatially converted to strings.
        '''
        if self._values:
            return self._values(record)
        msg = self.format(record)
        location = '{}:{}'.format(record.pathname, record.lineno)
        if record.exc_info:
            lines = ['Traceback (most recent call last):\n']
            lines += traceback.format_tb(record.exc_info[2])
            lines.append('{}: {}'.format(record.exc_info[0].__name__,
                         str(record.exc_info[1])))
            tb = ''.join(lines)
            if not tb.endswith('\n'):
                tb += '\n'
        else:
            tb = ''
        return msg, location, tb

