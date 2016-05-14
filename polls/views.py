from django.shortcuts import render
import re
import json
import sys
from elasticsearch import Elasticsearch

# Create your views here.

from django.http import HttpResponse, HttpResponseBadRequest,  HttpResponseNotFound


def index(request):
	if request.method != "GET":
		return HttpResponseBadRequest(json.dumps({"error": "Invalid request"}))

	query = request.GET.get('q', '')
	try:
		offset = int(request.GET.get('offset', 0))
		size = int(request.GET.get('size', 10))
	except ValueError:
		return HttpResponseBadRequest(json.dumps({"error": "Invalid request"}))

	match_all = False

	#with open("credentials") as f:
	#	user_id, password = f.readlines()[0].split(',')
	#	password = password.strip()

	if query:
		body = {"query": {"query_string": {"query": query, "fields": ['name', 'full_address']}}}
	else:
		match_all = True
		body = {"query": {"match_all": {}}}

	es = Elasticsearch('http://ec2-54-173-213-231.compute-1.amazonaws.com:9200',
		http_auth=('jay_cloyd_2016_05_11', 'wWEZC0KIfMG2'))
	results = es.search(index = 'jay_cloyd_2016_05_11_index', body=body, size = 10000)

	return_dict = dict()
	return_dict['businesses'] = list()
	return_dict['total'] = len(results['hits']['hits'])

	for businesses in results['hits']['hits']:
		new_dict = dict()
		new_dict['name'] = businesses['_source']['name']
		new_dict['id'] = businesses['_source']['business_id']
		new_dict['full_address'] = businesses['_source']['full_address']
		if not match_all:
			new_dict['score'] = businesses['_score']
		if businesses['_source'].get('checkin_info'):
			new_dict['total_checkins'] = sum(businesses['_source']['checkin_info'].itervalues())
		else:
			new_dict['total_checkins'] = 0
		return_dict['businesses'].append(new_dict)

	def sort_criteria(k):
		if match_all:
			return k['total_checkins']
		else:
			return (k['score'], k['total_checkins'])

	return_dict['businesses'] = sorted(return_dict['businesses'], key=sort_criteria, reverse=True)
	if not match_all:
		for result in return_dict['businesses']:
			result.pop('score', None)

	if offset * 10 < size:
		return_dict['businesses'] = return_dict['businesses'][offset * 10:size]
	else:
		return_dict['businesses'] = list()

	return HttpResponse(json.dumps(return_dict))