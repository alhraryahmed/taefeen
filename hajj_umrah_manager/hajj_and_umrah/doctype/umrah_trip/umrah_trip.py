# Copyright (c) 2026, Al-Taefeen Hajj & Umrah Services
# License: MIT

import frappe
from frappe.model.document import Document


class UmrahTrip(Document):
	def before_save(self):
		self.refresh_trip_stats()

	def refresh_trip_stats(self):
		"""تجميع عدد المعتمرين والمصاريف والإيرادات والأرباح من كل حجوزات هذه الرحلة"""
		if not self.name or self.is_new():
			# قبل أول حفظ لا توجد حجوزات مرتبطة بعد
			self.total_pilgrims = 0
			self.total_expenses_all = 0
			self.total_revenue_all = 0
			self.total_profit_all = 0
			return

		bookings = frappe.get_all(
			"Umrah Booking",
			filters={"umrah_trip": self.name, "docstatus": ["!=", 2]},
			fields=["total_expenses", "umrah_price", "total_profit"],
		)

		self.total_pilgrims = len(bookings)
		self.total_expenses_all = sum(b.total_expenses or 0 for b in bookings)
		self.total_revenue_all = sum(b.umrah_price or 0 for b in bookings)
		self.total_profit_all = sum(b.total_profit or 0 for b in bookings)


def refresh_trip_stats_on_booking_change(doc, method=None):
	"""يُستدعى من hooks عند تغيير أي حجز عمرة مرتبط برحلة، لتحديث ملخص الرحلة تلقائياً"""
	if doc.umrah_trip:
		trip = frappe.get_doc("Umrah Trip", doc.umrah_trip)
		trip.refresh_trip_stats()
		trip.db_update()
