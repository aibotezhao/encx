# -*- coding: utf-8 -*-
from __future__ import absolute_import
try:
    # py3
    from urllib.parse import quote, unquote
except Exception:
    # py2
    from urllib import quote, unquote

def encode(text):
    return quote(text.encode("utf-8"))

def decode(text, strict=False):
    s = text
    if strict and '%' in s:
        import re
        bad = re.search(r'%(?![0-9A-Fa-f]{2})', s)
        if bad:
            raise ValueError("Invalid percent-escape at pos %d" % bad.start())
    out = unquote(s)
    try:
        return out.decode("utf-8")
    except Exception:
        return out  # already str on py3
