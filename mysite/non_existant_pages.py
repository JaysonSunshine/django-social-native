from django.shortcuts import render
import json

# Create your views here.

from django.http import HttpResponse, HttpResponseBadRequest,  HttpResponseNotFound


def index(request):
	#raw_uri = request.get_raw_uri()
	return HttpResponseNotFound(json.dumps({"error": "Not found"}))
