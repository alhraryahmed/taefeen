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
fixtures = [
	{
		"doctype": "Role",
		"filters": [["name", "in", ["Hajj Umrah Manager"]]],
	},
	"Custom HTML Block",
	"Client Script",
	"Server Script",
	"Custom Field",
	"Property Setter",
	"Workspace"
]

# Document Events
# ---------------
doc_events = {}

# Website Context
# ---------------
website_context = {}
