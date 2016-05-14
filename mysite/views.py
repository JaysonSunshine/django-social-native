from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseBadRequest,  HttpResponseNotFound


def index(request):
	#raw_uri = request.get_raw_uri()
	return HttpResponse("This server responds to GET requests on the /businesses index")
