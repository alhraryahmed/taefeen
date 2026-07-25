# Copyright (c) 2026, Al-Taefeen Hajj & Umrah Services
# License: MIT

import frappe
from frappe.utils import flt


@frappe.whitelist()
def get_dashboard_stats():
	"""يعيد مؤشرات الأداء الرئيسية لبلوك الداشبورد"""

	total_pilgrims = frappe.db.count("Pilgrim")

	total_trips = frappe.db.count("Umrah Trip", filters={"docstatus": ["!=", 2]})

	treasury_balance = flt(frappe.db.get_single_value("Company Treasury", "current_balance"))

	profit_and_paid = frappe.db.sql(
		"""select coalesce(sum(total_profit), 0), coalesce(sum(total_paid), 0)
		from `tabUmrah Booking`
		where docstatus != 2""",
		as_list=True,
	)[0]

	return {
		"total_pilgrims": total_pilgrims,
		"total_trips": total_trips,
		"current_treasury_balance": treasury_balance,
		"total_profit": flt(profit_and_paid[0]),
		"total_collected": flt(profit_and_paid[1]),
	}
