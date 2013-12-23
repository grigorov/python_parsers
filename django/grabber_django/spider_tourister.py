# coding: utf-8
import csv
import logging
import re


from grab.spider import Spider, Task

import sys
import os

sys.path.append('.')
sys.path.append('./grabber_django')

os.environ['DJANGO_SETTINGS_MODULE'] = 'grabber_django.settings'
from django.conf import settings
from experts_tourister.models import Profile


class TouristerSpider(Spider):
    # Список страниц, с которых Spider начнёт работу
    # для каждого адреса в этом списке будет сгенерировано
    # задание с именем initial
    #initial_urls = ['http://experts.tourister.ru/mexico/busines']
    initial_urls = ['http://experts.tourister.ru/all_country']


    def task_initial(self,grab,task):
        print "список стран переводчиков"
        grab.setup(hammer_mode=True, hammer_timeouts=((2, 5), (10, 15), (20, 30)))
        for elem in grab.doc.select('//div[@class="expert-index-listfull"]/h2/a'):
            elem_url = elem.attr('href')
            match = "/guides"
            replace = "/busines"
            sourceCaseMatch = re.findall(match, elem_url, re.IGNORECASE)[0]
            url_country = elem_url.replace(sourceCaseMatch, replace)
            main_domain = 'http://experts.tourister.ru/'
            url = main_domain+url_country
            print "URL Country: %s" % url
            yield Task('init',url=url)
    def task_init(self, grab, task):
        print u'Список переводчиков:'

        # Это функция обработчик для заданий с именем initial
        # т.е. для тех заданий, чтобы были созданы для
        # адреов указанных в self.initial_urls

        # Как видите интерфейс работы с ответом такой же
        # как и в обычном Grab
        grab.setup(hammer_mode=True, hammer_timeouts=((2, 5), (10, 15), (20, 30)))
        for elem in grab.doc.select('//div[@class="guid-list__item guid-list__item-licenced-not"]/h3/a'):
            # Для каждой ссылки-заголовка создадим новое задание
            # с именем habrapost
            # Обратите внимание, что мы создаём задания с помощью
            # вызова yield - это сделано исключительно ради красоты
            # По-сути это равносильно следующему коду:
            # self.add_task(Task('habrapost', url=...))
            yield Task('profileurl', url=elem.attr('href'))

    def task_profileurl(self, grab, task):
        print 'Контактная информация: %s' % task.url

        # Эта функция, как вы уже догадываетесь
        # получает результаты обработки запросов, кооторые
        # мы создали для кадого хабратопика, найденного на
        # главной странице хабры

        # Для начала сохраним адрес и заголовк топика в массив
        profile = {
            'url': task.url+'/contacts',
        #    'title': grab.xpath_text('//h1/span[@class="post_title"]'),
        }

        # Теперь создадим запрос к поиску картинок яндекса, обратите внимание,
        # что мы передаём объекту Task информацию о хабрапосте. Таким образом
        # в функции обработки поиска картинок мы будем знать, для какого именно
        # хабрапоста мы получили результат поиска картинки. Дело в том, что все
        # нестандартные аргументы конструктора Task просто запоминаются в созданном
        # объекте и доступны в дальнейшем как его атррибуты
        #query = urllib.quote_plus(post['title'].encode('utf-8'))
        #search_url = 'http://images.yandex.ru/yandsearch?text=%s&rpt=image' % query
        #yield Task('image_search', url=search_url, post=post)
        print profile['url']
        yield Task('profile',url=profile['url'])
    def task_profile(self,grab,task):
        grab.setup(hammer_mode=True, hammer_timeouts=((2, 5), (10, 15), (20, 30)))
        print 'парсинг странц переводчиков:'
        try:
            interpreter_tel = grab.doc.select('//div[@class="nt-gid-linfo-tel"]//b').text()

        except IndexError:
            print 'not found tel'
            interpreter_tel = ''
        try:
            interpreter_name = grab.doc.select('//div[@class="nt-gid-linfo-zag"]/a').text()
        except IndexError:
            interpreter_name = ''
            print 'not found name'
        try:
            interpreter_city = grab.doc.select('//div[@class="nt-gid-linfo-city"]').text()
        except IndexError:
            print 'not found city'
            interpreter_city = ''
        try:
            interpreter_email = grab.doc.select('//div[@class="nt-gid-linfo-email"]/a').text()
        except IndexError:
            print 'not found email'
            interpreter_email = ''
        print "Interpreter Name: ", interpreter_name
        print "Interpreter Tel: ", interpreter_tel
        print "Interpreter Email: ", interpreter_email
        print "Interpreter City:", interpreter_city
        p = Profile(name=interpreter_name,country=interpreter_city,email=interpreter_email,telephone=interpreter_tel,url_profile=task.url)
        p.save()
    def task_image_search(self, grab, task):
        print 'Images search result for %s' % task.post['title']

        # В этой функции мы получили результат обработки поиска картинок, но
        # это ещё не сама картинка! Это только список найденных картинок,
        # Теперь возьмём адрес первой картинки и создадим задание для её
        # скачивания. Не забудем передать информацию о хабрапосте, для которого
        # мы ищем картинку, эта информация хранится в `task.post`.
        image_url = grab.xpath_text('//div[@class="b-image"]/a/img/@src')
        yield Task('image', url=image_url, post=task.post)

    def task_image(self, grab, task):
        print 'Image downloaded for %s' % task.post['title']

        # Это последнняя функция в нашем парсере.
        # Картинка получена, можно сохранить результат.
        path = 'images/%s.jpg' % self.result_counter
        grab.response.save(path)
        self.result_file.writerow([
            task.post['url'].encode('utf-8'),
            task.post['title'].encode('utf-8'),
            path
        ])
        # Не забудем увеличить счётчик ответов, чтобы
        # следующая картинка записалась в другой файл
        self.result_counter += 1


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # Запустим парсер в многопоточном режиме - два потока
    # Можно больше, только вас яндекс забанит
    # Он вас и с двумя то потоками забанит, если много будете его беспокоить
    bot = TouristerSpider(thread_number=10)
    bot.run()