from elasticsearch import Elasticsearch

import frappe
from   frappe import _

def doctype_to_index(doctype):
    index = doctype.tolower()
    index = doctype.replace(' ', '')

    return index

class ESearch(object):
    def __init__(self):
        self.esearch   = Elasticsearch()
        self.connected = self.esearch.ping()

    def search(self, query, indices = [ ], meta = [ ], filters = [ ], limit = 10,
        pagination   = 1):
        response     = [ ]

        indices      = ", ".join(indices) if indices else "_all"
        response     = self.esearch.search(indices)
        
        return response

def search(query, types = [ ], fields = [ ], filters = [ ], limit = 10,
	pagination = 1):
    esearch = ESearch()
    if esearch.connected:
        indices = [doctype_to_index(doctype) for doctype in types]

        results = esearch.search(query = query, indices = indices, meta = fields,
            filters = filters, limit = limit, pagination = pagination)
        return results
    else:
        frappe.throw(_("Unable to connect to Elastic Search"))
    