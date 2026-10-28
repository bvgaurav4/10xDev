#!/usr/bin/env python3
"""Execute a Python snippet or file in a namespace with json, sg, glob, importlib, shutil, os and Path available.

The executed code may assign its final value to the `result` variable; that value is printed as JSON.
"""
import argparse
import glob
import importlib
import json
import os
import shutil
from pathlib import Path

from swegemma import graph as sg


def execute(code: str):
    namespace = {
        "json": json,
        "sg": sg,
        "glob": glob,
        "importlib": importlib,
        "shutil": shutil,
        "os": os,
        "Path": Path,
        "result": None,
        "__name__": "__main__",
    }
    exec(compile(code, "<custom_script>", "exec"), namespace, namespace)
    return namespace["result"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--code", help="Python source code to execute")
    source.add_argument("--file", help="Path to a Python file to execute")
    args = parser.parse_args()

    code = args.code if args.code is not None else Path(args.file).read_text(encoding="utf-8")
    result = execute(code)
    print(json.dumps({"result": result}, default=str))


if __name__ == "__main__":
    main()
