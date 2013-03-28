
import json, time
from math import log
from urllib import quote_plus
import urllib2


_COUNT_URL = 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q='
_AUTOCOMPLETE_URL = 'http://suggestqueries.google.com/complete/search?client=chrome&q='


_last_query_time = 0.0
_QUERY_DELAY = 0.5
_FAIL_DELAY = 5.0

def urlopen(url):
    '''
    Let's avoid aggravating Google...
    '''
    global _last_query_time
    now = time.time()
    dt = now - _last_query_time
    if dt < _QUERY_DELAY:
        time.sleep(_QUERY_DELAY - dt)
    _last_query_time = time.time()
    return urllib2.urlopen(url)


def count_pages(q):
    '''
    Returns the number of search results Google returns for the given query.
    '''
    status = 0
    response = None
    while status != 200:
        response = json.load(urlopen(_COUNT_URL + quote_plus(q)))
        status = response['responseStatus']
        if status != 200:
            time.sleep(_FAIL_DELAY)
            print 'Failed! Retrying query...'
    return int(response['responseData']['cursor']['resultCount'].replace(
            ',',''))


def ngd(x, y):
    '''
    Normalized Google Distance
    http://arxiv.org/abs/cs.CL/0412098
    '''
    fx, fy, fxy = map(count_pages, (x, y, x+' '+y))
    log_fx, log_fy, log_fxy = map(log, (fx, fy, fxy))
    n = 1 # FIXME

    return ((max(log_fx, log_fy) - log_fxy) / 
            (log(n) - min(log_fx, log_fy)))


def relevancy(x, y):
    return (float(count_pages(x+' '+y)) /
        min(count_pages(x), count_pages(y)))


def autocomplete(q):
    results = json.load(urlopen(_AUTOCOMPLETE_URL + quote_plus(q)))
    return [val for val in results[1] if val.startswith(q)]

