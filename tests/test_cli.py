# -*- coding: utf-8 -*-
from __future__ import print_function
import subprocess, sys, os

PY = sys.executable

def run(cmd, data=b""):
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=data)
    if p.returncode != 0:
        sys.stderr.write(err.decode("utf-8", "ignore"))
    return p.returncode, out

def test_base64_roundtrip():
    data = b"hello\x00world"
    rc, enc = run([PY, "-m", "encx.cli", "base64", "encode"], data=data)
    assert rc == 0
    rc, dec = run([PY, "-m", "encx.cli", "base64", "decode"], data=enc)
    assert rc == 0 and dec == data

def test_hex_roundtrip():
    data = b"\x00\x01\x02abc"
    rc, enc = run([PY, "-m", "encx.cli", "hex", "encode"], data=data)
    assert rc == 0
    enc = enc.strip()
    rc, dec = run([PY, "-m", "encx.cli", "hex", "decode"], data=enc)
    assert rc == 0 and dec == data

def test_rot13():
    rc, out = run([PY, "-m", "encx.cli", "rot13", "encode"], data=b"uryyb")
    assert rc == 0 and out.strip() == b"hello"

def test_url():
    rc, out = run([PY, "-m", "encx.cli", "url", "encode"], data=b"a b+c?")
    assert rc == 0 and out.strip() == b"a%20b%2Bc%3F"

def test_xor():
    data = b"secret data"
    rc, enc = run([PY, "-m", "encx.cli", "xor", "encode", "-k", "key"], data=data)
    assert rc == 0
    rc, dec = run([PY, "-m", "encx.cli", "xor", "decode", "-k", "key"], data=enc)
    assert rc == 0 and dec == data
