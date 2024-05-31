import frappe


# api/method/athb.athb.doctype.api.getCountries
@frappe.whitelist(allow_guest=True)
def getCountries():
    data = frappe.db.sql(
        """
        SELECT *
        FROM `tabCountry` 
        """, 
        as_dict=1
                            )

    return data