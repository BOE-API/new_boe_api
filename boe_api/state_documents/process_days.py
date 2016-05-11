import datetime
from boe_api.state_documents.models import Documento
from boe_api.state_documents.tasks import daterange, process_next_day_summary

__author__ = 'carlos'



""" Process remaining days to process """

def process_remaining_days_summary():
    #last_day = Documento.objects.latest('fecha_publicacion').fecha_publicacion
    last_day = None
    if not last_day:
        last_day = datetime.date(year=2016, month=2, day=1)
    else:
        last_day = last_day.date()

    until = datetime.date(year=2016, month=2, day=3)
    #until = datetime.date.today()
    for day in daterange(last_day, until):
        print("not celery", day)
        process_next_day_summary.delay(day)
