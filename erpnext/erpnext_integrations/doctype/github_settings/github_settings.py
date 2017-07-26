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
				dict(label='GitHub Issue', insert_after='github_details')
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
				for milestone in repo.get_milestones():
					frappe.publish_realtime('msgprint', dict(title='Progress', indicator='green', clear=1,
						message = 'Adding milestone {0}'.format(frappe.bold(milestone.title))))
					project_name = frappe.db.get_value('Project',
						dict(github_milestone=milestone.number, github_repository=repo.full_name))
					if not project_name:
						project = frappe.get_doc(dict(
							doctype='Project',
							project_name=milestone.title,
							notes=milestone.description,
							status=milestone.state.title(),
							github_milestone=milestone.number,
							github_repository=repo.full_name,
						)).insert()
					else:
						project = frappe.get_doc('Project', project_name)

					# issues
					added = []
					for issue in repo.get_issues(milestone=milestone, state='all'):
						frappe.publish_realtime('msgprint', dict(title='Progress', indicator='green', clear=1,
							message = 'Adding issue {0}'.format(frappe.bold(issue.title))))
						issue_name = frappe.get_value('Task', dict(github_issue=issue.number))

						if issue_name:
							task = frappe.get_doc('Task', issue_name)
						else:
							task = frappe.new_doc('Task')

						task.subject = issue.title
						task.description = issue.body
						task.github_issue = issue.number
						task.project = project.name
						task.status = 'Open' if issue.state == 'open' else 'Closed'
						task.save()

						added.append(task.name)

					# set the rest as closed
					added = [project.name] + added
					frappe.db.sql('''
						update
							tabTask
						set
							status = 'Closed'
						where
							project = %s
							and name not in ({0})
						'''.format(', '.join(['%s'] * (len(added) - 1))), added)

	def get_repos(self):
		for d in self.repositories:
			yield self.get_github().get_user(d.user).get_repo(d.repository)

	def get_github(self):
		if not hasattr(self, '_github'):
			self._github = Github(self.username, self.get_password('password'))

		return self._github

@frappe.whitelist()
def sync():
	frappe.get_doc('GitHub Settings').sync()
