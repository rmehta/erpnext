frappe.listview_settings['Quotation'] = {
	add_fields: ["customer_name", "base_grand_total", "status",
		"company", "currency"],
	get_indicator: function(doc) {
		if(doc.status==="Submitted") {
			return [__("Submitted"), "blue", "status,=,Submitted"];
		} else if(doc.status==="Ordered") {
			return [__("Ordered"), "green", "status,=,Ordered"];
		} else if(doc.status==="Lost") {
			return [__("Lost"), "darkgrey", "status,=,Lost"];
		}
	},
	refresh: function(list) {
		new frappe.ui.Tour({
			name: 'new_quotation',
			steps: [{
				title: __('Create a new Customer Quote'),
				content: __('Click on new to create your first quotation'),
				element: '.page-head:visible .btn-primary:visible'
			}]
		});
	}
};
