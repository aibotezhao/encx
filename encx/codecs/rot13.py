# -*- coding: utf-8 -*-
from __future__ import absolute_import
import codecs

def transform(text):
    return codecs.decode(text, "rot_13")
