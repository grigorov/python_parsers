#!/usr/bin/python
#-*- encoding: Utf-8 -*-
from requests import get
from re import sub
from sys import stdout

html = get('http://www.hidemyass.com/proxy-list/').content
html = html.split('<table id="listtable"')[1].split('</table')[0]
html = html.split('<tr')[2:]

checkClass = lambda x: x.group(2) if x.group(1) not in classesBad else ''

for tr in html:
    css = tr.split('<style>\n')[1].split('\n<')[0].split('\n')

    classesBad = [rule[1:5] for rule in css if 'display:none' in rule]

    ip = tr.split('</style>')[1].split('</span></td>')[0]
    ip = sub('<(?:span|div) style="display:none">.+?</(?:span|div)>', '', ip)
    ip = sub('<span style="display: inline">(.+?)</span>', r'\1', ip)
    ip = sub('<span class="(.+?)">(.+?)</span>', checkClass, ip)
    ip = ip.replace('<span></span>', '')

    port = tr.split('<td>\n')[1].split('<')[0]

    protocol = tr.split(' \n             <td>')[1].split('<')[0].lower()

    print '%s://%s:%s/' % (protocol, ip, port)
