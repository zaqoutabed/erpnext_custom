import frappe
from frappe.utils import time_diff_in_hours

def attendance_validate(doc, method):
    if not doc.check_in or not doc.check_out:
        doc.hours = 0
        doc.status = "Absent"
        return
    working_hours = time_diff_in_hours(doc.check_out, doc.check_in)
    if working_hours < 0:
        frappe.throw("Check-out must be after Check-in")
    doc.hours = working_hours