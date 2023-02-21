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

def sales_invoice_validate(doc, method):
    invoice_notes = []
    for item in doc.items:
        if item.notes and len(item.notes) > 0:
            item.notes = get_clean_notes(item.notes)
            invoice_notes.append(item.notes)

    invoice_notes = "\n".join(invoice_notes)
    if len(invoice_notes) > 0:
        doc.remarks = invoice_notes

def get_clean_notes(notes):
    return "\n".join([line for line in ' '.join(notes.split()).split("\n") if notes and len(notes) > 0])