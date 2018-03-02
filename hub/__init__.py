from __future__ import absolute_import

import logging

import frappe
from   hub.__attr__ import *
from   hub.util import get_if_empty, safe_json_loads

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def get_user(access_token):
	hub_user_name = frappe.db.get_value('Hub User', {'access_token': access_token})
	if not hub_user_name:
		frappe.throw('Invalid access token', frappe.PermissionError)
	return hub_user_name

@frappe.whitelist(allow_guest = True)
def search(query, types = [ ], fields = [ ], filters = [ ], limit = 10, page = 1):
	"""
	Hub Search API
	"""
	from hub.engine import search
	
	types, fields, filters = safe_json_loads(types, fields, filters)
	parameters = dict(types = types, fields = fields, filters = filters,
		limit = limit, page = page)

	log.debug("hub.search: Parameters - {}".format(parameters))

	results = search(query, **parameters)

	return results
