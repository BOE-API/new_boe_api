import datetime
import logging
import re
import traceback
from boe_api.state_documents.models import Documento
import redis
from boe_api.state_documents.processDocument import ProcessDocument
from boe_api.taskapp.celery import app_celery, logger
from pattern.web import URL
from lxml import etree

import requests
from bs4 import BeautifulSoup

__author__ = 'carlos'

log = logging.getLogger('django')


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def processDay(d, url, url_boe, url_borme):
    print d
    url_day = getURLDay(d, url)
    print url_day
    req = requests.get(url_day)
    html = BeautifulSoup(req.text)
    link = html.find(href=re.compile("xml"))
    if link:
        url_sum = 'http://www.boe.es' + link.get('href')
        log.info(url_sum)
        procesarSumario(url_sum, url_boe)

@app_celery.task
def processDocument(url):
    try:
        d = ProcessDocument(url)
        d.saveDoc()
    except Exception, e:
        traceback.print_exc()
        print "fallo " + url


def getURLDay(d, urlS):
    mes = "%0*d" % (2, d.month)
    dia = "%0*d" % (2, d.day)
    url_day = urlS.format(d.year, mes, dia)
    return url_day


def procesarSumario(url_sumario, url_boe):
    url_sumario = url_sumario
    print url_sumario
    content = URL(url_sumario).download()
    xml = etree.XML(content)
    ids = etree.XPath("//item/@id")
    for id in ids(xml):
        url_doc = url_boe.format(id)
        processDocument.delay(url_doc)

@app_celery.task
def process_next_day_summary(day):

    today = day
    log.info(today)
    url = "http://www.boe.es/boe/dias/{0}/{1}/{2}/"
    url_borme = "http://www.boe.es/borme/dias/{0}/{1}/{2}/"
    url_boe = "http://www.boe.es/diario_boe/xml.php?id={0}"
    log.info(today)
    processDay(today, url, url_boe, url_borme)
    return True