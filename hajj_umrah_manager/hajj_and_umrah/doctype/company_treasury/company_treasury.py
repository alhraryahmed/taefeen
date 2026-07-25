# Copyright (c) 2026, Al-Taefeen Hajj & Umrah Services
# License: MIT

import frappe
from frappe.model.document import Document
from frappe.utils import flt, now_datetime


class CompanyTreasury(Document):
	pass


def _get_treasury():
	treasury = frappe.get_single("Company Treasury")
	if not treasury.treasury_name:
		treasury.treasury_name = "الخزينة الرئيسية"
	return treasury


def add_treasury_income(amount):
	"""إضافة مبلغ (إيراد) إلى رصيد الخزينة الحقيقي"""
	treasury = _get_treasury()
	treasury.current_balance = flt(treasury.current_balance) + flt(amount)
	treasury.last_updated = now_datetime()
	treasury.save(ignore_permissions=True)


def deduct_treasury_expense(amount):
	"""خصم مبلغ (مصروف) من رصيد الخزينة الحقيقي"""
	treasury = _get_treasury()
	treasury.current_balance = flt(treasury.current_balance) - flt(amount)
	treasury.last_updated = now_datetime()
	treasury.save(ignore_permissions=True)
