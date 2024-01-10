# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _
from odoo.exceptions import AccessError
from odoo.tests.common import Form

from .common import TestProjectTaskRestrictedFieldsCommon


class TestProjectTaskRestrictedFields(TestProjectTaskRestrictedFieldsCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        restrict_fields = cls.model_fields_obj.search(
            [
                ("model", "=", "project.task"),
                ("name", "in", cls.SELF_WRITE_RESTRICTED_FIELDS),
            ]
        )

        config = cls.config_obj.create({"restricted_field_ids": restrict_fields.ids})
        config.execute()

    def test_get_restricted_fields(self):
        """Test setting the default restricted fields in General Settings."""

        restricted_field_ids = self.config_parameter_obj.get_param(
            "project_task_restrict_field_update.restricted_field_ids"
        )
        restrict_fields = list(map(int, restricted_field_ids.split(",")))
        actual = set(self.model_fields_obj.browse(restrict_fields).mapped("name"))
        expected = set(self.SELF_WRITE_RESTRICTED_FIELDS)
        self.assertEqual(actual, expected, msg="Must be equal RESTRICTED FIELDS")

    def test_edit_task(self):
        """Check user edit restricted field"""

        task_form = Form(self.task_1.with_user(self.user_2))
        field_name = self.task_1._fields.get("name").string
        msg = _("You are not allowed to modify the '%(f)s' field") % {"f": field_name}
        with self.assertRaisesRegex(AccessError, msg):
            task_form.name = "Task 11"
            task_form.save()
