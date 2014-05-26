import datetime
import json
import re
import zipfile

# dependencies
import dateutil.tz
import pytz

def open(filename):
  with zipfile.ZipFile(filename) as fp:
    jslist = sorted(filter(lambda f: re.compile(r'^data/js/tweets/.+\.js$').match(f), fp.namelist()))
    ret = []
    for f in jslist:
      ret += reversed(json.loads(re.compile(r'.+?\n').sub("", fp.read(f).decode("ascii"), 1)))
    return ret

def parse_created_at(created_at):
  return datetime.datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S +0000")\
                 .replace(tzinfo = pytz.timezone("UTC")).astimezone(dateutil.tz.tzlocal())
