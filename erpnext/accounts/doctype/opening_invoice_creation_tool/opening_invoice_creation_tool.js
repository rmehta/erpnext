// Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Opening Invoice Creation Tool', {
	setup: (frm) => {
		frm.set_query('party_type', 'invoices', function(doc, cdt, cdn) {
			return {
				filters: {
					'name': ['in', 'Customer,Supplier']
				}
			}
		});
	},

	refresh: (frm) => {
		frm.disable_save();
		frm.page.set_primary_action(__("Make Invoice"), function() {
			return frm.call({
				doc: frm.doc,
				freeze: true,
				method: "make_invoices",
				freeze_message: __("Creating {0} Invoice", [frm.doc.invoice_type]),
				callback: function(r) {
				}
			});
		});
	},

	invoice_type: (frm) => {
		$.each(frm.doc.invoices, (idx, row) => {
			row.party_type = frm.doc.invoice_type == "Sales"? "Customer": "Supplier";
			row.party = "";
		});
		frm.refresh_fields();
	}
});

frappe.ui.form.on('Opening Invoice Creation Tool Item', {
	invoices_add: (frm) => {
		$.each(frm.doc.invoices, (idx, row) => {
			row.party_type = frm.doc.invoice_type == "Sales"? "Customer": "Supplier";
		});
	}
})