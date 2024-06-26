# Copyright (c) 2024, edom ibrahim and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Teacher(Document):

	def before_save(self):
		self.full_name = f"{self.first_name} {self.father_name} {self.last_name}"

	# def on_update(self):
	# 	self.full_name = f"{self.first_name} {self.father_name} {self.last_name}"
