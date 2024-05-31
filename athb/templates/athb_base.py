# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import frappe

# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import frappe

sitemap = 1


def get_context(context):
	print(frappe.session.user)
	frappe.set_user_lang(frappe.session.user,"ar")


	context.boot["lang"] = "ar"
	count = frappe.db.count('Landing Page')

	if count > 0:
		context.doc = frappe.get_last_doc("Landing Page")
	else:
		context.doc = frappe.new_doc("Landing Page")
	return context