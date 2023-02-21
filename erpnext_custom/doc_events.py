import frappe
from frappe.utils import time_diff_in_hours, flt

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
    validate_pos_payments(doc)
    update_sales_invoice_remarks(doc)
    

def validate_pos_payments(doc):
    if doc.is_pos == 0: return
    if len(doc.payments) <= 0:
        frappe.throw("Please add at least one payment")
    for payment in doc.payments:
        if flt(payment.amount) <= 0:
            frappe.throw("Payment amount must be greater than 0")

def update_sales_invoice_remarks(doc):
    invoice_notes = []
    for item in doc.items:
        if item.notes and len(item.notes) > 0:
            item.notes = get_clean_notes(item.notes)
            invoice_notes.append(item.notes)
    if len(invoice_notes) <= 0: return
    invoice_notes = "\n".join(invoice_notes)
    if len(invoice_notes) > 0:
        doc.remarks = invoice_notes

def get_clean_notes(notes):
    return "\n".join([line for line in ' '.join(notes.split()).split("\n") if notes and len(notes) > 0])