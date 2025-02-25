# Copyright 2025 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import Command, tools
from odoo.tests import tagged
from odoo.addons.base.tests.common import HttpCaseWithUserPortal
from odoo.addons.project.tests.test_access_rights import TestProjectPortalCommon
from lxml import html

@tagged("-at_install", "post_install")
class TestPortalProjectTaskCode(TestProjectPortalCommon, HttpCaseWithUserPortal):
    @classmethod
    def setUpClass(cls):
        super(TestPortalProjectTaskCode, cls).setUpClass()
        cls.task_1.project_id.privacy_visibility = "portal"
        task_wizard = cls.env['portal.share'].create({
            'res_model': 'project.task',
            'res_id': cls.task_1.id,
            'partner_ids': [
                Command.link(cls.partner_portal.id),
            ],
        })
        task_wizard.action_send_mail()

        cls.host = "127.0.0.1"
        cls.port = tools.config["http_port"]
        cls.base_url = "http://%s:%d/my/tasks/" % (cls.host, cls.port)
        cls.url_task_code_pattern = "/my/tasks/{}?"

    def test_portal_tasks_list_access(self):
        self.authenticate("portal", "portal")
        response = self.url_open(self.base_url)
        content = response.content
        tree = html.fromstring(content)
        spans = tree.xpath("//td[contains(@class, 'text-start') and contains(., '#')]//span")
        list_tasks_code = [s.text for s in spans]
        self.assertIn(self.task_1.code, list_tasks_code)
        link = tree.xpath(f"//td[a/span[contains(text(), '{self.task_1.name}')]]//a")[0].attrib['href']
        self.assertEqual(link,self.url_task_code_pattern.format(self.task_1.code))

    def test_portal_task_access(self):
        self.authenticate("portal", "portal")
        response = self.url_open(self.base_url + self.task_1.code)
        content = response.content
        tree = html.fromstring(content)
        spans = tree.xpath("//small[contains(@class, 'text-muted') and contains(@class, 'd-md-inline')]//span")
        list_tasks_code = [s.text for s in spans]
        self.assertIn(self.task_1.code, list_tasks_code)

    def test_portal_task_not_found(self):
        self.authenticate("portal", "portal")
        response = self.url_open(self.base_url + "NoCode")
        home_url = "http://%s:%d/my" % (self.host, self.port)
        self.assertEqual(response.url, home_url)

    def test_portal_task_search_link_format(self):
        self.authenticate("portal", "portal")
        task_code = self.task_1.code
        query_params = f"?search_in=ref&search={task_code}"
        response = self.url_open(self.base_url[:-1] + query_params)
        content = response.content
        tree = html.fromstring(content)
        spans = tree.xpath("//td[contains(@class, 'text-start') and contains(., '#')]//span")
        list_tasks_code = [s.text for s in spans]
        self.assertIn(task_code, list_tasks_code)
        link = tree.xpath(f"//td[a/span[contains(text(), '{self.task_1.name}')]]//a")[0].attrib['href']
        self.assertEqual(link, self.url_task_code_pattern.format(self.task_1.code)[:-1] + query_params)


