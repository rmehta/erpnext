frappe.ui.form.on('C-Form', {
	setup: (frm) => {
		frm.set_query('invoice_no', 'invoices', (doc) => {
			return {
				filters: {
					"docstatus": 1,
					"customer": doc.customer,
					"company": doc.company,
					"c_form_applicable": 'Yes',
					"c_form_no": ''
				}
			};
		});
	},
});

frappe.ui.form.on('C-Form Invoice Detail', {
	invoice_no: (frm) => {
		if (frm.doc.invoice_no) {
			frappe.call({
				method: 'erpnext.accounts.doctype.c_form.c_form.get_invoice_details',
				args: {
					invoice_no: frm.doc.invoice_no
				},
				callback: (r) => {
					frm.set_value(r.message);
				}
			});
		}
	}
});
