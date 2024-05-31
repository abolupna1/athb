import frappe

sitemap = 1
no_cache = 1

def get_context(context):
	count = frappe.db.count('Landing Page')
	if count > 0:
		context.doc = frappe.get_last_doc("Landing Page")
	else:
		context.doc = frappe.new_doc("Landing Page")
	return context