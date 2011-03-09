import os
import tempfile
import time
import re
from datetime import datetime, timedelta, tzinfo
try:
    import simplejson as json
except ImportError:
    import json

# this is a utility toolkit to perform data analysis on couchdb. couchdb temp views are
# excruciatingly slow. this toolkit dumps the entire db into memory in python, where
# you can process it quickly as you wish.

dumpfile = None
db = None

def get_couch_url(db, server, user, passwd):
    if len(server.split(':')) == 1:
        server += ':5984'

    cred = '%s:%s@' % (user, passwd) if user and passwd else ''
    return 'http://%s%s/%s/_all_docs?include_docs=true' % (cred, server, db)

def temp_filename():
    (fd, path) = tempfile.mkstemp()
    f = os.fdopen(fd)
    f.close()
    return path

def dumpdb(db, server='localhost', user=None, passwd=None):
    """call this to extract the database into a temp file. 'dumpfile' will be
    set to the temp file path"""
    global dumpfile
    dumpfile = temp_filename()

    url = get_couch_url(db, server, user, passwd)
    fetch_cmd = 'wget -O %s --progress=dot:mega %s 1>&2' % (dumpfile, url)
    os.popen(fetch_cmd)

def load(path=None, convert=True):
    """parse the dump file and load the data into memory. 'db' will be set to
    the loaded data"""
    global db

    if not path:
        path = dumpfile
    if not path:
        raise ValueError('no path to db dumpfile!')

    start = time.time()

    raw = json.load(open(path))
    db = [row['doc'] for row in raw['rows']]
    if convert:
        db = convert_data(db)

    end = time.time()

    print 'data loaded: %d docs, %.2fs' % (len(db), end - start)

def convert_data(e):
    """recursively convert parsed json into easy wrappers"""
    if isinstance(e, type({})):
        for k in e.keys():
            e[k] = convert_data(e[k])
        return EasyDict(e)
    elif hasattr(e, '__iter__'):
        return [convert_data(c) for c in e]
    else:
        try:
            e = parse_date(e)
        except (ValueError, TypeError):
            pass

        return e

class EasyDict(object):
    """helper object to work with json dicts more intuitively.
    given source dict 'd' and EasyDict e:
    e = EasyDict(d)
    e.x == d['x']
    e('#x') == d['#x']
    e._ == d
    e('_') == d['_']
    """

    def __init__(self, _dict):
        self.__dict__ = _dict

    def __call__(self, key):
        if key == '_':
            return self.__dict__[key]
        else:
            return self.__getattribute__(key)

    def __getattribute__(self, key):
        if key == '_':
            return self.__dict__
        else:
            return super(EasyDict, self).__getattribute__(key)

    def __repr__(self):
        return repr(self._)

def parse_date(s):
    for pattern, parsefunc in DATE_REGEXP:
        match = pattern.match(s)
        if match:
            return parsefunc(**match.groupdict())
    raise ValueError('did not match any date pattern')

def parse_iso_date(p):
    return datetime.strptime(p, '%Y-%m-%d').date()

def parse_iso_timestamp(p, frac, tz):
    return parse_full_timestamp('%Y-%m-%dT%H:%M:%S', p, frac, tz)

def parse_js_timestamp(p, tz):
    return parse_full_timestamp('%b %d %Y %H:%M:%S', p, None, tz)

def parse_full_timestamp(pattern, p, frac, tz):
    stamp = datetime.strptime(p, pattern)
    if frac:
        stamp += timedelta(seconds=float(frac))
    if tz:
        try:
            stamp = stamp.replace(tzinfo=TZ(tz))
        except ValueError:
            pass
    return stamp

DATE_REGEXP = [
    (re.compile('(?P<p>\d{4}-\d{2}-\d{2})$'), parse_iso_date),
    (re.compile('(?P<p>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(?P<frac>\.\d+)?(?P<tz>Z|[+-]\d{2,4})?$'), parse_iso_timestamp),
    (re.compile('\w{3} (?P<p>\w{3} \d{2} \d{4} \d{2}:\d{2}:\d{2}) (GMT|UTC)?(?P<tz>[+-]\d{4})'), parse_js_timestamp),
]

#do i really have to define this myself???
class TZ(tzinfo):
    def __init__(self, tz):
        if tz in ('Z', 'UTC'):
            tz = '+0000'

        self.name = tz
        try:
            sign = {'+': 1, '-': -1}[tz[0]]
            h = int(tz[1:3])
            m = int(tz[3:5]) if len(tz) == 5 else 0
        except:
            raise ValueError('invalid tz spec')
        self.offset = sign * (60 * h + m)

    def utcoffset(self, dt):
        return timedelta(minutes=self.offset)

    def tzname(self, dt):
        return self.name

    def dst(self, dt):
        return timedelta()

    def __repr__(self):
        return self.name









def dumpall(o):
    if isinstance(o, EasyDict):
        for k, v in o._.iteritems():
            for p in dumpall(v):
                yield p
    elif hasattr(o, '__iter__'):
        for e in o:
            for p in dumpall(e):
                yield p
    else:
        yield o
