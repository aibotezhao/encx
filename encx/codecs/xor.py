# -*- coding: utf-8 -*-
from __future__ import absolute_import
from itertools import cycle

def apply(data, key):
    if not key:
        raise ValueError("Key must not be empty")
    # ensure both are bytes
    return bytes(bytearray((ord(b) if isinstance(b, type(u"")) else b) ^ (ord(k) if isinstance(k, type(u"")) else k)
                           for b, k in zip(data, cycle(key))))
