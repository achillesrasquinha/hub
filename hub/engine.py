from elasticsearch import Elasticsearch

import frappe
from   frappe import _

class ESearch(object):
    def __init__(self):
        self.esearch = Elasticsearch()
        self.ok      = self.esearch.ping()

    def search(self, query, indices = [ ], meta = [ ], filters = [ ], limit = 10,
        pagination = 1):
        response     = "barfoo"

        return response

def search(query, types = [ ], fields = [ ], filters = [ ], limit = 10,
	pagination = 1):
    esearch = ESearch()
    if esearch.ok:
        results = esearch.search(query = query, indices = types, meta = fields,
            filters = filters, limit = limit, pagination = pagination)
        return results
    else:
        frappe.throw(_("Unable to connect to Elastic Search"))
    