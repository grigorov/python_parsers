from grab import Grab
from grab.tools.logs import default_logging
default_logging()

g = Grab()
#g.go('http://rus-afrika.tourister.ru/contacts')
g.go('http://ndavous.tourister.ru/contacts')
#g.go('http://gerald.tourister.ru/contacts')
#g.go('http://myjapan.org/contacts')
#g.go('http://guide-in-japan.ru/contacts')
try:
    interpreter_tel = g.doc.select('//div[@class="nt-gid-linfo-tel"]//b').text()

except IndexError:
    print 'not found tel'
    interpreter_tel = ''

try:
    interpreter_name = g.doc.select('//div[@class="nt-gid-linfo-zag"]/a').text()
except IndexError:
    interpreter_name = ''
    print 'not found name'
try:
    interpreter_city = g.doc.select('//div[@class="nt-gid-linfo-city"]').text()
except IndexError:
    print 'not found city'
    interpreter_city = ''
try:
    interpreter_email = g.doc.select('//div[@class="nt-gid-linfo-email"]/a').text()
except IndexError:
    print 'not found email'
    interpreter_email = ''



print "Interpreter Name: ", interpreter_name
print "Interpreter Tel: ", interpreter_tel
print "Interpreter Email: ", interpreter_email
print "Interpreter City:", interpreter_city
