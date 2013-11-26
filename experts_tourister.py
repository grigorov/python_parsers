#/usr/bin/env python
import urllib
import lxml.html
import datetime
from datetime import date, time

from pony import *
from pony.orm import *

db = Database('mysql', db='test', user='root', passwd='')

class Interpreter(db.Entity):
    _table_ = 'interpreters'
    id = PrimaryKey(int, auto=True)
    name =  Required(str)
    email = Optional(str,unique=True)
    Country = Optional(str)
    City = Optional(str)
    tel = Optional(str)
    other_contact = Optional(str)
    is_resume = Optional(bool)

db.generate_mapping(create_tables=True)

if __name__ == "__main__":
    print "Parser for experts_tourister.ru"
    with db_session:
    	test = Interpreter(name="test",email="admin@test.com",tel="79053721214", is_resume=True)
    	print select(u for u in Interpreter)
