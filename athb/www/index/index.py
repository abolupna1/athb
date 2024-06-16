import frappe

sitemap = 1
no_cache = 1

def get_context(context):
	count = frappe.db.count('Landing Page')
	prices = frappe.get_all("Athb Pricing",fields=['name','title', 'price','high_light'],order_by='sort asc',
)
	context.pricing = []
	
	for price in prices:
		details =[]
		doc = frappe.get_doc("Athb Pricing", price.name)
		for child_doc in doc.details:
			details.append({
				'title':child_doc.title
			})
		


		context.pricing.append({
			"title":price.title,
			"price":price.price,
			"high_light":price.high_light,
			"details": details
		})
	
	if count > 0:
		context.doc = frappe.get_last_doc("Landing Page")
	else:
		context.doc = frappe.new_doc("Landing Page")

	return context
