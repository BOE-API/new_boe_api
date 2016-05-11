from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from boe_api.state_documents.process_days import process_remaining_days_summary


def process_all(request):
    process_remaining_days_summary()
    return HttpResponse(status=200)