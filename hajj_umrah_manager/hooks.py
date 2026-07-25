app_name = "hajj_umrah_manager"
app_title = "Hajj Umrah Manager"
app_publisher = "Al-Taefeen Hajj & Umrah Services"
app_description = "نظام إدارة المعتمرين والحجوزات والأقساط والخزينة - شركة الطائفين لخدمات الحج والعمرة"
app_email = "info@altaefeen.example.com"
app_license = "MIT"
app_version = "0.1.0"

# Includes in <head>
# ------------------
app_include_css = "/assets/hajj_umrah_manager/css/hajj_umrah_dashboard.css"

# Fixtures
# --------
# دور مخصص لموظفي شركة الحج والعمرة (بدون صلاحيات System Manager الكاملة)
fixtures = [
	{
		"doctype": "Role",
		"filters": [["name", "in", ["Hajj Umrah Manager"]]],
	}
]

# Document Events
# ---------------
# ملاحظة: منطق التزامن الأساسي (تحديث الخزينة عند الدفع، تحديث ملخص الرحلة)
# مُنفَّذ مباشرة داخل controllers الخاصة بكل DocType (on_update / on_submit)
# لتفادي التعقيد الزائد لنظام صغير. هذا القسم متروك جاهزاً لأي تكاملات مستقبلية
# (مثل الربط مع Sales Invoice / Payment Entry في محاسبة ERPNext).
doc_events = {}

# Website Context (لعرض بلوك الداشبورد كصفحة Jinja اختيارية)
# -----------------------------------------------------------
website_context = {}
