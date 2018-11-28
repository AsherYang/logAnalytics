# -*- coding:utf-8 -*-

import sys
sys.path.append('../')

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import gzip, json, urllib, urllib2, collections, time, logging
import json
import ssl

context = ssl._create_unverified_context()


def http_get(url, params={}, header={}):
    httpUrl = url
    if params is not None and len(params) > 0:
        httpUrl = url + "?" + _encode_params(**params)
    httpUrl = httpUrl.replace(': ', ':')
    httpUrl = httpUrl.replace(', ', ',')
    httpUrl = httpUrl.replace("'", '"')
    # print httpUrl
    req = urllib2.Request(httpUrl, None, headers=header)
    res = urllib2.urlopen(req)
    body = _read_body(res)
    logging.info('-----> body: ' + body)
    return body


def http_post(url, params={}, header={}):
    params = json.dumps(params)
    print 'param : ', params
    req = urllib2.Request(url, params, headers=header)
    res = urllib2.urlopen(req, context=context)
    body = _read_body(res)
    return body


def _encode_params(**kw):
    params = []
    for k, v in kw.iteritems():
        if isinstance(v, basestring):
            qv = v.encode('utf-8') if isinstance(v, unicode) else v
            params.append('%s=%s' % (k, urllib.quote(qv)))
        elif isinstance(v, collections.Iterable):
            for i in v:
                qv = i.encode('utf-8') if isinstance(i, unicode) else str(i)
                params.append('%s=%s' % (k, urllib.quote(qv)))
        else:
            qv = str(v)
            params.append('%s=%s' % (k, urllib.quote(qv)))
    return '&'.join(params)


def _read_body(res):
    using_gzip = res.headers.get('Content-Encoding', '') == 'gzip'
    body = res.read()
    if using_gzip:
        gzipper = gzip.GzipFile(fileobj=StringIO(body))
        body = gzipper.read()
        gzipper.close()
    return body
