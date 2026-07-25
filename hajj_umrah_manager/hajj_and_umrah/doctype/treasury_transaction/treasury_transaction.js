// Copyright (c) 2026, Al-Taefeen Hajj & Umrah Services
// License: MIT

frappe.ui.form.on("Treasury Transaction", {
	refresh(frm) {
		if (frm.is_new()) {
			frm.set_value("transaction_type", frm.doc.transaction_type || "Expense");
		}
		if (frm.doc.docstatus === 1) {
			frm.dashboard.set_headline(
				frm.doc.transaction_type === "Income"
					? __("تم إضافة هذا المبلغ إلى رصيد الخزينة")
					: __("تم خصم هذا المبلغ من رصيد الخزينة")
			);
		}
	},
});
