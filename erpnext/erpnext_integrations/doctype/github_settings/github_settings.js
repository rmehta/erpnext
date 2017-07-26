// Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('GitHub Settings', {
	refresh: function(frm) {
		frm.add_custom_button(__('Sync'), () => {
			return frappe.call({
				method: 'erpnext.erpnext_integrations.doctype.github_settings.github_settings.sync'
			});
		});
	}
});
