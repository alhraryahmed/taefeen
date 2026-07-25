// Copyright (c) 2026, Al-Taefeen Hajj & Umrah Services
// License: MIT

frappe.ui.form.on("Umrah Booking", {
	refresh(frm) {
		if (frm.doc.payment_type === "Cash" && !frm.is_new()) {
			frm.add_custom_button(__("تسجيل دفعة كاش"), () => {
				frappe.prompt(
					[
						{
							fieldname: "amount",
							fieldtype: "Currency",
							label: __("المبلغ المستلم"),
							reqd: 1,
						},
					],
					(values) => {
						frm.set_value("total_paid", flt(frm.doc.total_paid) + flt(values.amount));
						frm.save();
					},
					__("تسجيل دفعة"),
					__("تأكيد")
				);
			}).addClass("btn-primary");
		}
	},

	payment_currency: recalc_expenses,
	exchange_rate: recalc_expenses,
	visa_cost: recalc_expenses,
	ticket_cost: recalc_expenses,
	makkah_housing_cost: recalc_expenses,
	madinah_housing_cost: recalc_expenses,
	transport_cost: recalc_expenses,
	umrah_price: recalc_expenses,

	payment_type(frm) {
		frm.refresh_field("installment_plan");
	},
});

function recalc_expenses(frm) {
	const total_expenses =
		flt(frm.doc.visa_cost) +
		flt(frm.doc.ticket_cost) +
		flt(frm.doc.makkah_housing_cost) +
		flt(frm.doc.madinah_housing_cost) +
		flt(frm.doc.transport_cost);

	const rate = flt(frm.doc.exchange_rate) || 1.0;
	const base_umrah_price = flt(frm.doc.umrah_price) * rate;

	frm.set_value("total_expenses", total_expenses);
	frm.set_value("base_umrah_price", base_umrah_price);
	frm.set_value("total_profit", base_umrah_price - total_expenses);
	frm.set_value("balance_amount", flt(frm.doc.umrah_price) - flt(frm.doc.total_paid));
}

frappe.ui.form.on("Installment Schedule Row", {
	paid_amount(frm) {
		let total_paid = 0;
		(frm.doc.installment_plan || []).forEach((row) => {
			total_paid += flt(row.paid_amount);
		});
		frm.set_value("total_paid", total_paid);
		frm.set_value("balance_amount", flt(frm.doc.umrah_price) - total_paid);
	},
});
