// Copyright (c) 2026, Al-Taefeen Hajj & Umrah Services
// License: MIT

frappe.ui.form.on("Umrah Trip", {
	refresh(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__("عرض حجوزات المعتمرين"), () => {
				frappe.set_route("List", "Umrah Booking", { umrah_trip: frm.doc.name });
			});

			frm.add_custom_button(__("إضافة حجز جديد لهذه الرحلة"), () => {
				frappe.new_doc("Umrah Booking", { umrah_trip: frm.doc.name });
			});
		}
	},
});
