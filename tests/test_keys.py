#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest.mock import MagicMock, patch

import chalicelib.keys as target


def test_key_cache_without_prefix():
    """ KeyCache オブジェクトで prefix なしのケース """
    s3 = MagicMock()
    s3.get_object.side_effect = ValueError('FAKE')

    with patch('secrets.token_bytes', return_value=b'0123456789ABCDEF'):
        cache = target.KeyCache(s3, 'dummy', 'https://example.com')
        assert cache.get('EXAMPLE', 'example') == b'0123456789ABCDEF'
        assert cache.url('EXAMPLE', 'example') == 'https://example.com/EXAMPLE/example'  # noqa


def test_key_cache_from_s3():
    """ KeyCache オブジェクトで s3 から値を取得するケース """
    stream = MagicMock()
    stream.read.return_value = b'AAAAAAAAAAAAAAAA'
    s3 = MagicMock()
    s3.get_object.return_value = {'Body': stream}

    with patch('secrets.token_bytes', return_value=b'0123456789ABCDEF'):
        cache = target.KeyCache(s3, 'dummy', 'https://example.com')
        assert cache.get('EXAMPLE', 'example') == b'AAAAAAAAAAAAAAAA'


def test_key_cache_with_prefix():
    """ KeyCache オブジェクトで prefix ありのケース """
    s3 = MagicMock()
    s3.get_object.side_effect = ValueError('FAKE')

    with patch('secrets.token_bytes', return_value=b'0123456789ABCDEF'):
        cache = target.KeyCache(s3, 'dummy', 'https://example.com', 'prefix')
        assert cache.get('EXAMPLE', 'example') == b'0123456789ABCDEF'
        assert cache.url('EXAMPLE', 'example') == 'https://example.com/prefix/EXAMPLE/example'  # noqa
