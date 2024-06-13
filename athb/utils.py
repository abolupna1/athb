
import frappe
def sendmail(doc,recipients,msg,title,template,attachments=None):
	email_args = {
				"recipients": recipients,
				"message": msg,
				"subject": title,
				"reference_doctype": doc.doctype,
				"reference_name": doc.name,
				"template":template
				}
	if attachments:email_args["attachments"]=attachments
	
	frappe.enqueue(method=frappe.sendmail, queue='short', timeout=300,  **email_args)