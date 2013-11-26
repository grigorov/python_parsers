#/usr/bin/env python
import urllib,socket
import lxml.html

site_pages = [
'http://www.proz.com/profile/125321',
'http://www.proz.com/profile/12525',
'http://www.proz.com/profile/19525',
'http://www.proz.com/profile/46214'
]
profile_list=[]
failed_pages = []
aval_pages = []


def create_list_profile():
    l = range(1755460,1755467)
    for x in l:
        link = 'http://www.proz.com/profile/'+ str(x)
        profile_list.append(link)
        print link

def check_pages(pages):
    try:
        for page_url in pages:
            code = urllib.urlopen(page_url).getcode()
            print "{0} - {1}".format(page_url, code)
            if (code not in [200, 301]):
                failed_pages.append(page_url)
            else:
                aval_pages.append(page_url)
    except socket.error, e:
        print "Ping Error: ", e

def generate_message():
    n = len(failed_pages)
    list = ""
    if (n > 0):
        list = "404 errors: \r\n"
        for failed_link in failed_pages:
            list = "\r\n".join((list, failed_link))
    else:
        list = "All links are correct"
    return list
def profile_pages():
    n = len(aval_pages)
    list = []
    if (n > 0):
        for live_profile in aval_pages:
            list.append(live_profile)
    else:
        return 0
    return list

def parse_page(page):
    p = urllib.urlopen(page)
    doc = lxml.html.document_fromstring(p.read())
    txt1 = doc.xpath('//*[@id="lang_sum"]/span[*]/span')
    txt2 = doc.xpath('/html/body/div[1]/div/table/tr/td/div/div/table/tr/td/table/tr/td[2]/table[1]/tr/td[1]/font/strong')
    langs=[]
    name = ''
    for fio in txt2:
        name = fio.text
        print name
    for txt in txt1:
        print txt.text
        langs.append(txt.text)
#        link_to_download = "http://nginx.org" + txt.get('href')
#    version = link_to_download.split("-")[1].split(".")
#    ver = version[0]+ "." + version[1] + "." + version[2]
#    return ver
def contact_info(page):
#    http://www.proz.com/?sp=profile&sp_mode=contact&eid_s=46214
    id = page.split("/")[4]
    profile_link = "http://www.proz.com/?sp=profile&sp_mode=contact&eid_s="+id
    print profile_link
    return profile_link
def parse_contact_info(page):
    p = urllib.urlopen(page)
    doc = lxml.html.document_fromstring(p.read())
    country = doc.xpath('//*[@id="countryView"]')
    city = doc.xpath('//*[@id="cityView"]')
    for c in country:
        print "Country:",c.text
    for ct in city:
        print "City:",ct.text

if __name__ == "__main__":
    print "Parser for Proz.com"
    create_list_profile()
    check_pages(profile_list)
    lists = profile_pages()
    for list in lists:
        parse_page(list)
        profile = contact_info(list)
        parse_contact_info(profile)
