# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import frappe

sitemap = 1


def get_context(context):
	count = frappe.db.count('Landing Page')
	prices = frappe.get_all("Athb Pricing",fields=['title', 'price','high_light'],order_by='sort asc',
)
	context.pricing = []
	
	for price in prices:
		context.pricing.append({
			"title":price.title,
			"price":price.price,
			"high_light":price.high_light,
			"details": frappe.get_all("Athb Pricing Details",fields=['title'],filters={
        'parent': price.name
    },)
		})
	if count > 0:
		context.doc = frappe.get_last_doc("Landing Page")
	else:
		context.doc = frappe.new_doc("Landing Page")
		context.pricing = frappe.get_all("Athb Pricing")

	return context
