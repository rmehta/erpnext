# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from github import Github

class GitHubSettings(Document):
	def on_update(self):
		if self.username and self.password:
			self.make_custom_fields()

	def make_custom_fields(self):
		'''if enabled create custom fields in Project'''
		from frappe.custom.doctype.custom_field.custom_field import create_custom_field
		custom_fields = {
			'Project': [
				dict(label='GitHub Details', fieldtype='Section Break', insert_after='append'),
				dict(label='GitHub Milestone', insert_after='github_details'),
				dict(label='GitHub Repository', insert_after='github_milestone')
			],
			'Task': [
				dict(label='GitHub Details', fieldtype='Section Break', insert_after='append'),
				dict(label='GitHub Issue', insert_after='github_details'),
				dict(label='GitHub Repository', insert_after='github_issue')
			]
		}
		for doctype, fields in custom_fields.items():
			for df in fields:
				create_custom_field(doctype, df)

	def sync(self):
		self.sync_projects()

	def sync_projects(self):
		if self.sync_projects_with_milestones:
			for repo in self.get_repos():
				# print repo.name, repo.full_name
				for m in repo.get_milestones():
					project_name = frappe.db.get_value('Project',
						dict(github_milestone=m.number, github_repository=repo.full_name))
					if not project_name:
						frappe.get_doc(dict(
							doctype='Project',
							project_name=m.title,
							notes=m.description,
							status=m.state.title(),
							github_milestone=m.number,
							github_repository=repo.full_name,
						)).insert()

	def get_repos(self):
		for d in self.repositories:
			yield self.get_github().get_user(d.user).get_repo(d.repository)

	def get_github(self):
		if not hasattr(self, '_github'):
			self._github = Github(self.username, self.get_password('password'))

		return self._github

def sync():
	frappe.get_doc('GitHub Settings').sync()
