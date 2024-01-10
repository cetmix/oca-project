# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase, tagged

WRITE_RESTRICTED_FIELDS = [
    "partner_id",
    "user_ids",
    "analytic_account_id",
    "name",
    "project_id",
    "milestone_id",
    "date_deadline",
    "tag_ids",
    "planned_hours",
    "priority",
    "parent_id",
    "date_end",
    "email_cc",
    "recurring_task",
]


@tagged("-at_install", "post_install")
class TestProjectTaskRestrictedFieldsCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.account_analytic_line_obj = cls.env["account.analytic.line"]
        project_project_obj = cls.env["project.project"]
        project_task_obj = cls.env["project.task"]
        res_partner_obj = cls.env["res.partner"]
        res_users_obj = cls.env["res.users"].with_context(no_reset_password=True)
        cls.config_obj = cls.env["res.config.settings"].sudo()
        cls.model_fields_obj = cls.env["ir.model.fields"].sudo()
        cls.config_parameter_obj = cls.env["ir.config_parameter"].sudo()

        multi_company_group = cls.env.ref("base.group_multi_company")
        project_user_group = cls.env.ref("project.group_project_user")

        cls.partner_1 = res_partner_obj.create({"name": "Test Partner #1"})
        cls.partner_2 = res_partner_obj.create({"name": "Test Partner #2"})

        cls.user_1 = res_users_obj.create(
            {
                "name": "User 1",
                "login": "user_1",
                "email": "user1@test.com",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            project_user_group.id,
                            multi_company_group.id,
                        ],
                    )
                ],
            }
        )

        cls.user_2 = res_users_obj.create(
            {
                "name": "User 2",
                "login": "user_2",
                "email": "user2@test.com",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            project_user_group.id,
                            multi_company_group.id,
                        ],
                    )
                ],
            }
        )

        cls.user_manager = res_users_obj.create(
            {
                "name": "User Officer",
                "login": "user_manager",
                "email": "usermanager@test.com",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            project_user_group.id,
                            multi_company_group.id,
                        ],
                    )
                ],
            }
        )

        cls.project_1 = project_project_obj.create(
            {
                "name": "Project #1",
                "user_id": cls.user_manager.id,
            }
        )
        cls.task_1 = project_task_obj.create(
            {
                "name": "Task 1",
                "project_id": cls.project_1.id,
            }
        )

    @classmethod
    @property
    def SELF_WRITE_RESTRICTED_FIELDS(cls):
        return WRITE_RESTRICTED_FIELDS
