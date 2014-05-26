import json
import re
import zipfile

def open(filename):
  with zipfile.ZipFile(filename) as fp:
    jslist = sorted(filter(lambda f: re.compile(r'^data/js/tweets/.+\.js$').match(f), fp.namelist()))
    ret = []
    for f in jslist:
      ret += reversed(json.loads(re.compile(r'.+?\n').sub("", fp.read(f).decode("ascii"), 1)))
    return ret
