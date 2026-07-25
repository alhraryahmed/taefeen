# Copyright (c) 2026, Al-Taefeen Hajj & Umrah Services
# License: MIT

import frappe
from frappe.model.document import Document

from hajj_umrah_manager.hajj_and_umrah.doctype.company_treasury.company_treasury import (
	add_treasury_income,
	deduct_treasury_expense,
)


class TreasuryTransaction(Document):
	def on_submit(self):
		if self.transaction_type == "Income":
			add_treasury_income(self.amount)
		else:
			deduct_treasury_expense(self.amount)

	def on_cancel(self):
		# عكس تأثير الحركة على الرصيد عند إلغاء الاعتماد
		if self.transaction_type == "Income":
			deduct_treasury_expense(self.amount)
		else:
			add_treasury_income(self.amount)
