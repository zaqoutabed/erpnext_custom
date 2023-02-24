frappe.ui.form.on('Quotation', {
    setup: function (frm) {
        frm.set_query("quotation_to", function () {
            return {
                filters: { "name": ["in", ["Customer"]] }
            }
        });
    }
})
