#/usr/bin/env python
import urllib
import lxml.html

failed_pages=[]
list_profiles = []
aval_pages = []
def create_list_profile():
    #http://www.translatorscafe.com/cafe/member75985.htm
    l = range(10000,10020)
    for x in l:
        link = 'http://www.translatorscafe.com/cafe/member'+ str(x)+'.htm'
        list_profiles.append(link)
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
    txt1 = doc.xpath('/html/body/table[1]/tr/td/table[2]/tr/td[2]/table[4]/tr[1]/td[2]')
    txt2 = doc.xpath('//*[@id="Profile_Start"]/tr/td[2]/h1/a')
    contact = doc.xpath('/html/body/table[1]/tr/td/table[2]/tr/td[2]/p[1]')
    langs=[]
    cn = []
    name = ''
    for fio in txt2:
        name = fio.text
        print "Name:",name
    for txt in txt1:
        print "Langs:",txt.text
        langs.append(txt.text)
    for con in contact:
        print "Contacts:",con.text
        cn.append(con.text)
#        link_to_download = "http://nginx.org" + txt.get('href')
#    version = link_to_download.split("-")[1].split(".")
#    ver = version[0]+ "." + version[1] + "." + version[2]
#    return ver

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
    print "Parser for Translatorcafe"
    create_list_profile()
    check_pages(list_profiles)
    lists = profile_pages()
    for list in lists:
        parse_page(list)
#        parse_contact_info(profile)


