# Copyright (c) 2026, Al-Taefeen Hajj & Umrah Services
# License: MIT

import frappe
from frappe import _
from frappe.model.document import Document


class Pilgrim(Document):
	def validate(self):
		self.validate_family_registration()

	def validate_family_registration(self):
		"""إذا كان التسجيل عائلياً، يجب اختيار ولي الأمر أو وجود أفراد عائلة"""
		if self.registration_type == "Family":
			if not self.head_of_family and not self.family_members:
				frappe.msgprint(
					_("يفضل تحديد ولي الأمر أو إضافة أفراد العائلة عند اختيار تسجيل عائلي"),
					alert=True,
					indicator="orange",
				)
