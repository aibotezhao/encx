# -*- coding: utf-8 -*-
from __future__ import absolute_import
import binascii

def encode(data):
    return binascii.hexlify(data)

def decode(data, strict=False):
    s = data.strip()
    if strict:
        # binascii will raise on non-hex or odd length
        return binascii.unhexlify(s)
    # lenient: if odd length, prefix a '0'
    if len(s) % 2 == 1:
        s = b"0" + s
    try:
        return binascii.unhexlify(s)
    except Exception as e:
        # best-effort: filter non-hex chars
        filtered = b"".join(ch for ch in s if ch in b"0123456789abcdefABCDEF")
        if len(filtered) % 2 == 1:
            filtered = b"0" + filtered
        return binascii.unhexlify(filtered)
