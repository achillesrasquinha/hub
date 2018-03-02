from __future__ import absolute_import

from elasticsearch import Elasticsearch

import frappe
from   frappe import _
from   hub.util import sequencify

def doctype_to_index(name):
    name = name.strip()           
    name = name.lower()           
    name = name.replace(' ', '-')

    return name

def index_to_doctype(name):
    name = name.strip()
    name = " ".join(name.split("-"))
    name = name.title()

    return name

def build_response(results):
    response = dict(
        results = [
            dict(
                 type = index_to_doctype(result['_index']),
                 name = result['_id'],
                score = result['_score']
            ) for result in results['hits']['hits']
        ],
        count   = result['total']
    )

    return response

class ESearch(object):
    def __init__(self):
        self.esearch   = Elasticsearch()
        self.connected = self.esearch.ping()

    def search(self, query, indices = [ ], source = [ ], filters = [ ], limit = 10, page = 1):
        indices  = ", ".join(indices) if indices else "_all"
        
        query    = { "query": { "match_all": { } } }
        response = self.esearch.search(indices, body = query)
        
        return response

def search(query, types = [ ], fields = [ ], filters = [ ], limit = 10, page = 1):
    esearch = ESearch()
    if esearch.connected:
        types    = sequencify(types)
        fields   = sequencify(fields)

        indices  = [doctype_to_index(doctype) for doctype in types]

        results  = esearch.search(query = query, indices = indices, source = fields,
            filters = filters, limit = limit, page = page)

        response = build_response(results)

        return response
    else:
        frappe.throw("Unable to connect to Elastic Search.")