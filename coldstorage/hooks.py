# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "coldstorage"
app_title = "Erpnext Cold Storage Warehouse Manager"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Cold Storage Warehouse Manager for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/coldstorage/css/coldstorage.bundle.css"
app_include_js = "/assets/coldstorage/js/coldstorage.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "coldstorage.engine.on_document_submit",
        "on_cancel": "coldstorage.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "coldstorage.engine.daily_scheduled_sync"
    ]
}
