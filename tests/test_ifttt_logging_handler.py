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

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import inspect
import logging

import mock
import pytest

from ifttt_logging_handler import IFTTTLoggingHandler


_log = logging.getLogger('test-logger')


def logger(key='my-key', event='my-event', *args, **kwargs):
    for handler in _log.handlers[:]:
        _log.removeHandler(handler)
    _log.setLevel(logging.NOTSET)
    handler = IFTTTLoggingHandler(key, event, *args, **kwargs)
    _log.addHandler(handler)
    return _log, handler


@mock.patch('ifttt_logging_handler.requests.post')
class TestIFTTTLoggingHandler(object):

    def test_key_and_event_in_url(self, post):
        log, _ = logger('my-key-?', 'my-event-:')
        log.error('foobar')
        assert post.call_count == 1
        url = post.call_args[0][0].lower()
        assert 'my-key-%3f' in url
        assert 'my-event-%3a' in url

    def test_default_values(self, post):
        log, handler = logger()
        handler.setFormatter(logging.Formatter('_%(message)s_'))
        log.error('oh noes')
        lineno = inspect.stack()[0][2] - 1
        assert post.call_count == 1
        data = post.call_args[1]['json']
        assert data['value1'] == '_oh noes_'
        assert data['value2'] == '{}:{}'.format(__file__, lineno)
        assert data['value3'] == ''

    def test_traceback(self, post):
        log, _ = logger()
        try:
            raise ValueError('oh noes')
        except Exception as e:
            log.exception('boom')
        assert post.call_count == 1
        tb = post.call_args[1]['json']['value3']
        assert 'Traceback' in tb
        assert 'ValueError: oh noes' in tb

    def test_custom_values_are_converted_to_string(self, post):
        def values(record):
            assert isinstance(record, logging.LogRecord)
            return 1, 2, 3
        log, _ = logger(values=values)
        log.error('oh noes')
        assert post.call_count == 1
        data = post.call_args[1]['json']
        assert data['value1'] == '1'
        assert data['value2'] == '2'
        assert data['value3'] == '3'

    def test_custom_value_is_converted_to_a_list(self, post):
        def values(record):
            assert isinstance(record, logging.LogRecord)
            return 'foo'
        log, _ = logger(values=values)
        log.error('oh noes')
        assert post.call_count == 1
        data = post.call_args[1]['json']
        assert data['value1'] == 'foo'
        assert data['value2'] == ''
        assert data['value3'] == ''

    def test_level(self, post):
        log, _ = logger()
        log.setLevel(logging.WARNING)
        log.info('foo')
        assert not post.called
        log, _ = logger(level=logging.WARNING)
        log.setLevel(logging.INFO)
        log.info('foo')
        assert not post.called
        log, _ = logger(level=logging.INFO)
        log.setLevel(logging.INFO)
        log.info('foo')
        assert post.called

