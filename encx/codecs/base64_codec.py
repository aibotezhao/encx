# -*- coding: utf-8 -*-
from __future__ import absolute_import
import base64
import re

_B64_RE = re.compile(br'^[A-Za-z0-9+/_-]+={0,2}$')

def encode(data, urlsafe=False):
    if urlsafe:
        return base64.urlsafe_b64encode(data).rstrip(b"\n")
    return base64.b64encode(data).rstrip(b"\n")

def decode(data, urlsafe=False, strict=False):
    s = data.strip()
    if strict and not _B64_RE.match(s.replace(b'-', b'+').replace(b'_', b'/')):
        raise ValueError("Invalid base64 characters in strict mode")
    fn = base64.urlsafe_b64decode if urlsafe else base64.b64decode
    try:
        return fn(s)
    except Exception:
        # try with padding
        pad = b'=' * ((4 - (len(s) % 4)) % 4)
        return fn(s + pad)
