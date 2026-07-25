# Copyright (c) 2026, Al-Taefeen Hajj & Umrah Services
# License: MIT

import frappe
from frappe.model.document import Document
from frappe.utils import add_months, flt, getdate, nowdate


class UmrahBooking(Document):
	def validate(self):
		self.calculate_expenses_and_profit()
		self.handle_installment_plan()
		self.calculate_total_paid()
		self.calculate_balance()
		self.set_status()

	# ---------------------------------------------------------------------
	# جدول المصاريف والتكاليف -> مجموع المصاريف وإجمالي المكسب
	# ---------------------------------------------------------------------
	def calculate_expenses_and_profit(self):
		self.total_expenses = (
			flt(self.visa_cost)
			+ flt(self.ticket_cost)
			+ flt(self.makkah_housing_cost)
			+ flt(self.madinah_housing_cost)
			+ flt(self.transport_cost)
		)
		rate = flt(self.exchange_rate) or 1.0
		self.base_umrah_price = flt(self.umrah_price) * rate
		self.total_profit = flt(self.base_umrah_price) - flt(self.total_expenses)

	# ---------------------------------------------------------------------
	# توليد جدول الأقساط (10 أشهر) تلقائياً عند اختيار الدفع بالتقسيط
	# ---------------------------------------------------------------------
	def handle_installment_plan(self):
		if self.payment_type != "Installments":
			self.installment_plan = []
			return

		if not self.umrah_price:
			return

		# لا نولّد الجدول من جديد إذا كان موجوداً بالفعل (حتى لا نفقد مدفوعات مسجلة سابقاً)
		if self.installment_plan and len(self.installment_plan) == 10:
			return

		self.set("installment_plan", [])
		monthly_amount = flt(self.umrah_price) / 10
		start_date = getdate(self.booking_date or nowdate())

		for i in range(1, 11):
			self.append(
				"installment_plan",
				{
					"month_number": i,
					"due_date": add_months(start_date, i),
					"installment_amount": monthly_amount,
					"paid_amount": 0,
					"payment_status": "Unpaid",
				},
			)

	# ---------------------------------------------------------------------
	# إجمالي المدفوع
	# ---------------------------------------------------------------------
	def calculate_total_paid(self):
		if self.payment_type == "Installments":
			total = 0
			for row in self.installment_plan:
				paid = flt(row.paid_amount)
				total += paid
				if paid <= 0:
					row.payment_status = "Unpaid"
				elif paid < flt(row.installment_amount):
					row.payment_status = "Partially Paid"
				else:
					row.payment_status = "Paid"
					if not row.payment_date:
						row.payment_date = nowdate()
			self.total_paid = total
		else:
			# الدفع كاش: القيمة تُدخل مباشرة (عبر واجهة الحجز) في total_paid
			self.total_paid = flt(self.total_paid)

	def calculate_balance(self):
		self.balance_amount = flt(self.umrah_price) - flt(self.total_paid)

	def set_status(self):
		if self.docstatus == 2:
			self.status = "Cancelled"
		elif self.docstatus == 0:
			self.status = "Draft"
		elif flt(self.balance_amount) <= 0:
			self.status = "Completed"
		else:
			self.status = "Confirmed"

	# ---------------------------------------------------------------------
	# مزامنة الدفعات مع الخزينة: أي زيادة في "إجمالي المدفوع" تتحول تلقائياً
	# إلى حركة إيراد مؤكدة في الخزينة، مرتبطة بهذا الحجز
	# ---------------------------------------------------------------------
	def on_update(self):
		self.sync_treasury_income()
		self.notify_trip_of_change()

	def sync_treasury_income(self):
		already_recorded = flt(
			frappe.db.sql(
				"""select coalesce(sum(amount), 0) from `tabTreasury Transaction`
				where reference_booking = %s and transaction_type = 'Income' and docstatus = 1""",
				self.name,
			)[0][0]
		)

		delta = flt(self.total_paid) - already_recorded
		if delta == 0:
			return

		txn = frappe.new_doc("Treasury Transaction")
		txn.transaction_type = "Income" if delta > 0 else "Expense"
		txn.amount = abs(delta)
		txn.reference_booking = self.name
		txn.description = (
			f"دفعة من المعتمر {self.pilgrim_name or self.pilgrim} - حجز {self.name}"
			if delta > 0
			else f"تصحيح/استرجاع دفعة - حجز {self.name}"
		)
		txn.insert(ignore_permissions=True)
		txn.submit()

	def notify_trip_of_change(self):
		if self.umrah_trip:
			from hajj_umrah_manager.hajj_and_umrah.doctype.umrah_trip.umrah_trip import (
				refresh_trip_stats_on_booking_change,
			)

			refresh_trip_stats_on_booking_change(self)
