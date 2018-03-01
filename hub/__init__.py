from __future__ import absolute_import

import frappe

__version__ = '0.0.1'

def get_user(access_token):
	hub_user_name = frappe.db.get_value('Hub User', {'access_token': access_token})
	if not hub_user_name:
		frappe.throw('Invalid access token', frappe.PermissionError)
	return hub_user_name

import logging

from frappe.chat.util import (
	assign_if_empty,
	safe_json_loads
)

log = logging.getLogger(__name__)

@frappe.whitelist(allow_guest = True)
def search(query, types = [ ], fields = [ ], filters = [ ], limit = 10,
	pagination = 1):
	from hub.engine import search
	
	types, fields, filters = safe_json_loads(types, fields, filters)

	results = search(query, types = types, fields = fields, filters = filters,
		limit = limit, pagination = pagination)

	return results
