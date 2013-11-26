#!/usr/bin/env python
import argparse
import cookielib
from HTMLParser import HTMLParser
import random
import socket; socket.setdefaulttimeout(5)
import sys
import urllib2

# http://techblog.willshouse.com/2012/01/03/most-common-user-agents/
USER_AGENTS = [
    'Mozilla/5.0 (X11; Linux x86_64; rv:10.0.2) Gecko/20100101 Firefox/10.0.2',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.2 (KHTML, like Gecko) Safari/125.8',
    'Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_1) AppleWebKit/536.25 (KHTML, like Gecko) Version/6.0 Safari/536.25',
    ]

BANNER = """
 _     _     _                                    
| |__ (_) __| | ___ _ __ ___  _   _  __ _ ___ ___ 
| '_ \| |/ _` |/ _ \ '_ ` _ \| | | |/ _` / __/ __|
| | | | | (_| |  __/ | | | | | |_| | (_| \__ \__ \\
|_| |_|_|\__,_|\___|_| |_| |_|\__, |\__,_|___/___/  Proxy Grabber
                              |___/               

Author: tullyvey based on the version by mich4th3c0wb0y of r00tw0rm
Published under WTFPL http://sam.zoy.org/wtfpl/COPYING
Greets: To youtube users ChRiStIaAn008 and dodo3773 :)
"""

def setup_http(proxy={'':''}):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.ProxyHandler(proxy), 
                                    urllib2.HTTPCookieProcessor(cj))
    # random userAgent
    opener.addheaders = [('User-Agent', random.choice(USER_AGENTS)),] 
    urllib2.install_opener(opener)


### HMA html parsing ###

class _HtmlHandler:
    def __init__(self, parser):
        self.parser = parser
    
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if (tag == 'table' and 'id' in attrs 
                and attrs['id'] == 'listtable'):
            return _TableHandler(self.parser)
        return self
    
    def handle_data(self, data): pass
    def handle_endtag(self, tag): return self


class _TableHandler(_HtmlHandler):
    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            if self.parser.firstrow: # skip the headers
                self.parser.firstrow = False
                return self
            return _RowHandler(self.parser) 
        return self
        
    def handle_endtag(self, tag):
        return _HtmlHandler(self.parser) if tag == 'table' else self


class _RowHandler(_HtmlHandler):               
    def handle_starttag(self, tag, attrs):
        if tag != 'td':
            return self
        # 0 = last update, 3 = country, 4 = speed, 
        # 5 = connection time, 7 = anonymity
        column_handlers = { 1: _IpHandler,
                        2: _PortHandler,
                        6: _ProtocolHandler,
                        }
        self.parser.columnidx += 1
        idx = self.parser.columnidx
        if idx in column_handlers:
            return column_handlers[idx](self.parser)
        return self
    
    def handle_endtag(self, tag): 
        if tag != 'tr': return self
        self.parser._add_proxy()
        self.parser.columnidx = -1
        return _TableHandler(self.parser)

        
class _IpHandler(_HtmlHandler):
    def __init__(self, parser):
        _HtmlHandler.__init__(self, parser)
        self.handle_data = self.handle_ignorable
        self.parser.ip = ''
        self.invisible_classes = []
    
    def handle_starttag(self, tag, attrs):
        if tag == 'style':
            self.handle_data = self.handle_style
        elif tag == 'div' or tag == 'span':
            attrs = dict(attrs)
            if (('style' not in attrs or 
                    attrs['style'] != 'display:none') and 
                ('class' not in attrs or 
                    attrs['class'] not in self.invisible_classes)):
                self.handle_data = self.handle_fragment
            else:
                self.handle_data = self.handle_ignorable
        return self
    
    def handle_ignorable(self, data):
        pass
    
    def handle_style(self, data):
        for line in data.split('\n'):
            line = line.strip()
            if not line.endswith('{display:none}'): continue
            self.invisible_classes.append(line[1:line.find('{')])
    
    def handle_fragment(self, data):
        self.parser.ip += data
    
    def handle_endtag(self, tag):
        if tag == 'style' or tag == 'div' or tag == 'span':
            self.handle_data = self.handle_fragment
        elif tag == 'td':
            return _RowHandler(self.parser)
        return self


class _PortHandler(_HtmlHandler):
    def handle_data(self, data):
        self.parser.port = int(data)
    
    def handle_endtag(self, tag):
        return _RowHandler(self.parser)


class _ProtocolHandler(_PortHandler):
    def handle_data(self, data):
        self.parser.protocol = data.strip().lower()


class ProxyListParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.state = _HtmlHandler(self)
        self.firstrow = True
        self.columnidx = -1
        self.ip = None
        self.port = None
        self.protocol = None
        self.proxy_list = []
        
    def _add_proxy(self):
        self.proxy_list.append((self.ip, self.port, self.protocol))
    
    def handle_starttag(self, tag, attrs):
        self.state = self.state.handle_starttag(tag, attrs)
    
    def handle_data(self, data):
        self.state.handle_data(data)
        
    def handle_endtag(self, tag):
        self.state = self.state.handle_endtag(tag)

### end HMA html parsing ###


def get_hma_proxies(page):
    print '### http://hidemyass.com/proxy-list/%d ###' % page
    setup_http()
    html = urllib2.urlopen('http://hidemyass.com/proxy-list/%d' % page).read()
    parser = ProxyListParser()
    parser.feed(html)
    return ["%s:%d" % (ip, port) for ip, port, protocol in 
                parser.proxy_list if protocol == 'http']


def get_new_proxy_list(nproxies, testurl):
    proxies = []
    page = 0
    
    while len(proxies) < nproxies:
        page += 1
        candidates = get_hma_proxies(page)
        
        for proxy in candidates:
            if proxy in proxies: continue
            setup_http({'http':'http://%s' % proxy})
            try:
                res = urllib2.urlopen(testurl)
                proxies.append(proxy)
                print 'ok: %s => %d'%(proxy, len(proxies))
            except Exception as e:
                print 'fail: %s [%s]'%(proxy, e)
            if len(proxies) >= nproxies:
                print 'finish'
                break

    return proxies


def write_proxy_list(proxies, filename):
    fd = open(filename, 'w')
    for proxy in proxies:
        fd.write('%s\n'%(proxy))
    fd.close()


def main():
    parser = argparse.ArgumentParser(description='Hidemyass Proxy Grabber',
        epilog='\n%s\n\nGrab 17 Proxies from hidemyass.com and save them to proxy.txt\n'\
        'make sure that all saved Proxies works with google.com\n\n'\
        'Example: python %s -f proxy.txt -n 17 -t http://google.com\n\n%s\n' % 
                                                    ( '-'*80, sys.argv[0], '-'*80),
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-f', action='store', dest='filename', 
                        help='Filename to store new Proxies' )
    parser.add_argument('-n', action='store', type=int, dest='nproxies', 
                        help='Number of proxies you want to grab' )
    parser.add_argument('-t', action='store', dest='testurl', 
                        help='URL to test for, like http://google.com' )

    args = parser.parse_args()
    print(BANNER)

    if not (args.filename and args.nproxies and args.testurl):
        parser.print_help()
        sys.exit(0)
    
    if not args.testurl.startswith('http://'):
        args.testurl = 'http://' + args.testurl
    
    proxies = get_new_proxy_list(args.nproxies, args.testurl)
    write_proxy_list(proxies, args.filename)


if __name__ == '__main__':
    main()
