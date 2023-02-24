frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {
        if(frm.is_new()===0){
            frm.trigger("toggle_discount");
        }
    },
    customer: function(frm) {
        frm.trigger("toggle_discount");
    },
    toggle_discount: function(frm) {
        if(frm.doc.customer){
            frappe.db.get_value("Customer", frm.doc.customer, "allow_discount").then(r => {
                const allow_discount = r && r.message && r.message.allow_discount || 0
                frm.events.handle_toggle_discount(frm, allow_discount);
            })
        }else{
            frm.events.handle_toggle_discount(frm, 0);
        }
    },
    handle_toggle_discount(frm, allow_discount){
        [
            'is_cash_or_non_trade_discount',
            'additional_discount_percentage',
            'discount_amount',
            'apply_discount_on',
        ].forEach(field => {
            frm.toggle_enable(field, allow_discount);
            if(field === 'apply_discount_on'){
                return
            }
            frm.set_value(field, 0);
            frm.refresh_field(field);
        });
    }
})
