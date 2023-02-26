import frappe
from frappe import _
from erpnext.buying.doctype.purchase_order.purchase_order import PurchaseOrder


class CustomPurchaseOrder(PurchaseOrder):
    def update_requested_qty(self):
        material_request_map = {}
        for d in self.get("items"):
            if d.material_request_item:
                material_request_map.setdefault(d.material_request, []).append(
                    d.material_request_item
                )

        for mr, mr_item_rows in material_request_map.items():
            if mr and mr_item_rows:
                mr_obj = frappe.get_doc("Material Request", mr)
                mr_obj.update_requested_qty(mr_item_rows)
