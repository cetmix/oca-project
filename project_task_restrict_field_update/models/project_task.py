from odoo import _, fields, models
from odoo.exceptions import AccessError


class ProjectTask(models.Model):
    _inherit = "project.task"

    can_write_restricted = fields.Boolean(
        compute="_compute_can_write_restricted",
        help="This field is used for conditional display of other fields on views",
    )

    def _compute_can_write_restricted(self):
        """Computes 'can_write_restricted' field values"""
        self.can_write_restricted = self._can_write_restricted()

    def _can_write_restricted(self):
        """Checks if user can update manager only fields
        Returns:
            Boolean: True is he/she can otherwise False
        """
        # Check if user is a member of the 'Project/Manager' group or is a superuser
        can_write_restricted = (
            self.env.user.has_group("project.group_project_manager")
            or self.env.user._is_superuser()
        )
        # Check if user is modifying tasks he didn't create himself
        if not can_write_restricted:
            tasks_not_created_by_user = self.filtered(
                lambda t: t.create_uid.id != self.env.uid
            )
            can_write_restricted = not bool(tasks_not_created_by_user)

        bypass_restriction = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("project_task_restrict_field_update.bypass_restriction", False)
        )
        # Check if user is modifying tasks he did create himself
        if not can_write_restricted:
            tasks_not_created_by_user = self.filtered(
                lambda t: t.create_uid.id == self.env.uid
            )
            can_write_restricted = bool(tasks_not_created_by_user) or bypass_restriction

        return can_write_restricted

    def _get_write_restricted_fields(self):
        """Returns a list of write restricted fields
        Returns:
            List of str: list of fields
        """
        ICPSudo = self.env["ir.config_parameter"].sudo()
        model_fields_obj = self.env["ir.model.fields"].sudo()
        restricted_field_ids = ICPSudo.get_param(
            "project_task_restrict_field_update.restricted_field_ids"
        )
        restrict_fields = list(map(int, restricted_field_ids.split(",")))
        return model_fields_obj.browse(restrict_fields).mapped("name")

    def write(self, vals):
        if not self._can_write_restricted():
            # Check if any of the manager only fields is updated
            restricted_fields = self._get_write_restricted_fields()
            for updated_field in vals.keys():
                if updated_field in restricted_fields:
                    # Get the field caption for the access error message
                    field_name = self._fields.get(updated_field).string
                    raise AccessError(
                        _("You are not allowed to modify the '%(f)s' field")
                        % {"f": field_name}
                    )
        return super().write(vals)
