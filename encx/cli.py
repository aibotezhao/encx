# -*- coding: utf-8 -*-
from __future__ import absolute_import
import argparse
import sys
from encx.codecs import base64_codec, hex_codec, rot13, url_codec, xor

CODECS = {
    "base64": base64_codec,
    "hex": hex_codec,
    "rot13": rot13,
    "url": url_codec,
    "xor": xor,
}

def _read_input(path):
    if path:
        with open(path, "rb") as f:
            return f.read()
    data = sys.stdin.read()  # bytes in py2, text/bytes in py3
    if isinstance(data, type(u"")) and sys.version_info[0] >= 3:
        return data.encode("utf-8", "surrogatepass")
    return data

def _write_output(data, outfile, is_textish):
    if outfile:
        with open(outfile, "wb") as f:
            f.write(data)
        return
    # stdout
    try:
        sys.stdout.write(data.decode("utf-8"))
    except Exception:
        # fallback to raw bytes
        if hasattr(sys.stdout, "buffer"):
            sys.stdout.buffer.write(data)
        else:
            sys.stdout.write(data)

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(prog="encx", description="encx: encodings and XOR (py27-compatible)")
    subparsers = parser.add_subparsers(dest="codec")
    # argparse required=True isn't available on older Pythons
    # base64
    p_b64 = subparsers.add_parser("base64", help="Base64 encode/decode")
    p_b64.add_argument("mode", choices=["encode", "decode"], nargs="?", default="encode")
    p_b64.add_argument("-f", "--file", help="Input file (defaults to stdin)")
    p_b64.add_argument("-o", "--out", help="Output file (defaults to stdout)")
    p_b64.add_argument("--strict", action="store_true", help="Strict mode for decoder (basic validation)")
    p_b64.add_argument("--urlsafe", action="store_true", help="Use URL-safe alphabet")
    p_b64.add_argument("--no-newline", action="store_true", help="Do not append newline for text outputs")

    # hex
    p_hex = subparsers.add_parser("hex", help="Hex encode/decode")
    p_hex.add_argument("mode", choices=["encode", "decode"], nargs="?", default="encode")
    p_hex.add_argument("-f", "--file", help="Input file (defaults to stdin)")
    p_hex.add_argument("-o", "--out", help="Output file (defaults to stdout)")
    p_hex.add_argument("--strict", action="store_true", help="Strict mode for decoder")
    p_hex.add_argument("--no-newline", action="store_true", help="Do not append newline for text outputs")

    # rot13
    p_rot = subparsers.add_parser("rot13", help="ROT13 for text (encode/decode are identical)")
    p_rot.add_argument("mode", choices=["encode", "decode"], nargs="?", default="encode")
    p_rot.add_argument("-f", "--file", help="Input file (defaults to stdin)")
    p_rot.add_argument("-o", "--out", help="Output file (defaults to stdout)")
    p_rot.add_argument("--strict", action="store_true", help="Strict UTF-8 decode")
    p_rot.add_argument("--no-newline", action="store_true", help="Do not append newline for text outputs")

    # url
    p_url = subparsers.add_parser("url", help="URL percent-encoding")
    p_url.add_argument("mode", choices=["encode", "decode"], nargs="?", default="encode")
    p_url.add_argument("-f", "--file", help="Input file (defaults to stdin)")
    p_url.add_argument("-o", "--out", help="Output file (defaults to stdout)")
    p_url.add_argument("--strict", action="store_true", help="Strict percent-escape checks")
    p_url.add_argument("--no-newline", action="store_true", help="Do not append newline for text outputs")

    # xor
    p_xor = subparsers.add_parser("xor", help="XOR stream using a repeating key")
    p_xor.add_argument("mode", choices=["encode", "decode"], nargs="?", default="encode")
    p_xor.add_argument("-f", "--file", help="Input file (defaults to stdin)")
    p_xor.add_argument("-o", "--out", help="Output file (defaults to stdout)")
    p_xor.add_argument("-k", "--key", required=True, help="Key as text or hex (see --key-hex)")
    p_xor.add_argument("--key-hex", action="store_true", help="Treat key as hexadecimal bytes")

    args = parser.parse_args(argv)
    if args.codec is None:
        parser.print_usage()
        return 2

    codec = CODECS[args.codec]
    raw = _read_input(getattr(args, "file", None))

    if args.codec == "base64":
        if args.mode == "encode":
            out = codec.encode(raw, urlsafe=getattr(args, "urlsafe", False))
        else:
            out = codec.decode(raw, urlsafe=getattr(args, "urlsafe", False), strict=getattr(args, "strict", False))
        textish = True
    elif args.codec == "hex":
        if args.mode == "encode":
            out = codec.encode(raw)
        else:
            out = codec.decode(raw, strict=getattr(args, "strict", False))
        textish = True
    elif args.codec == "rot13":
        s = raw.decode("utf-8") if getattr(args, "strict", False) else raw.decode("utf-8", "replace")
        out = codec.transform(s).encode("utf-8")
        textish = True
    elif args.codec == "url":
        if args.mode == "encode":
            s = raw.decode("utf-8") if getattr(args, "strict", False) else raw.decode("utf-8", "replace")
            out = codec.encode(s).encode("ascii")
        else:
            s = raw.decode("ascii", "ignore")
            out = codec.decode(s, strict=getattr(args, "strict", False)).encode("utf-8")
        textish = True
    elif args.codec == "xor":
        if getattr(args, "key_hex", False):
            try:
                import binascii
                key_bytes = binascii.unhexlify(args.key.strip())
            except Exception:
                sys.stderr.write("Invalid hex for --key.\n")
                return 1
        else:
            key_bytes = args.key.encode("utf-8")
        out = codec.apply(raw, key_bytes)
        textish = False
    else:
        sys.stderr.write("Unknown codec.\n")
        return 1

    if textish and not getattr(args, "out", None) and not getattr(args, "no-newline", False):
        if not out.endswith(b"\n"):
            out += b"\n"

    _write_output(out, getattr(args, "out", None), textish)
    return 0

if __name__ == "__main__":
    sys.exit(main())
