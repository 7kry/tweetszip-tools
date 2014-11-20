import datetime
import json
import re
import zipfile

# dependencies
import dateutil.tz
import pytz

# Const
CSV_SCHEMA = [
  "tweet_id",
  "in_reply_to_status_id",
  "in_reply_to_user_id",
  "timestamp",
  "source",
  "text",
  "retweeted_status_id",
  "retweeted_status_user_id",
  "retweeted_status_timestamp",
  "expanded_urls",
]

JSON_TSFORMAT = "%a %b %d %H:%M:%S %z %Y"
CSV_TSFORMAT = "%Y-%m-%d %H:%M:%S %z"

def status_to_csvrow(status):
  return [
    status['id'],                                                                     # tweet_id
    status.get('in_reply_to_status_id', ''),                                          # in_reply_to_status_id
    status.get('in_reply_to_user_id', ''),                                            # in_reply_to_user_id
    status['created_at'],                                                             # timestamp
    status['source'],                                                                 # source
    status['text'],                                                                   # text
    status['retweeted_status']['id'] if 'retweeted_status' in status else "",         # retweeted_status_id
    status['retweeted_status']['user']['id'] if 'retweeted_status' in status else "", # retweeted_status_user_id_
    status['retweeted_status']['created_at'] if 'retweeted_status' in status else "", # retweeted_status_timestamp
    ",".join(map(lambda url: url['expanded_url'], status['entities']['urls'])),       # expanded_urls
  ]

def open(filename):
  with zipfile.ZipFile(filename) as fp:
    jslist = sorted(filter(lambda f: re.compile(r'^data/js/tweets/.+\.js$').match(f), fp.namelist()))
    ret = []
    for f in jslist:
      ret += reversed(json.loads(re.compile(r'.+?\n').sub("", fp.read(f).decode("ascii"), 1)))
    return ret

def parse_created_at(created_at):
  try:
    t = datetime.datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S +0000")
  except ValueError:
    t = datetime.datetime.strptime(created_at, "%a %b %d %H:%M:%S +0000 %Y")
  return t.replace(tzinfo = pytz.timezone("UTC")).astimezone(dateutil.tz.tzlocal())
