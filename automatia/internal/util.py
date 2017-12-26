import re
import imp

from automatia.internal.legal_tlds import *


def flatten(array):
    return [val for sublist in array for val in sublist]


ul = r'\u00a1-\uffff'

url_re = re.compile(
    r'^(?:(?:[a-z0-9.\-+]*)://)?'  # scheme is validated separately
    # r'(?:\S+(?::\S*)?@)?'  # user:pass authentication
    r'(?:(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}|\[[0-9a-f:.]+\]|'
    r'(' +
    (
        r'[a-z' +
        ul +
        r'0-9](?:[a-z' +
        ul +
        r'0-9-]{0,61}[a-z' +
        ul +
        r'0-9])?'
    ) +
    (
        r'(?:\.(?!-)[a-z' +
        ul +
        r'0-9-]{1,63}(?<!-))*'
    ) +
    (
        r'\.'  # dot
        r'((?!-)' +  # can't start with a dash
        r'(?:[a-z{}-]'.format(ul) +  # domain label
        r'{2,63}|xn--[a-z0-9]{1,59})'  # or punycode label
        r'(?<!-)'  # can't end with a dash
        r'\.?'  # may have a trailing dot
    ) +
    ')'
    r'))'
    r'(?::\d{2,5})?'  # port
    r'(?:[/?#][^\s]*)?'  # resource path
    r'\Z', re.IGNORECASE
)


def is_url(s):
    m = url_re.match(s)
    return m is not None and m.group(2) in TLDS


def import_exists(package):
    try:
        imp.find_module(package)
        return True
    except ImportError:
        return False
