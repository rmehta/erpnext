# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SalesLedgerEntry(Document):
	def on_update(self):
		# update % delivered for sales order
		if self.is_delivery:
			total_delivered = frappe.db.sum('Sales Ledger Entry', 'qty', dict(sales_order = self.sales_order, is_delivered =1))