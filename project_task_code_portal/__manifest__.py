# Copyright 2025 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Project Task Code Portal",
    "summary": "Use custom task code in customer portal",
    "version": "16.0.1.0.0",
    "development_status": "Beta",
    "category": "Project",
    "website": "https://github.com/OCA/project",
    "author": "Cetmix OÜ, Odoo Community Association (OCA)",
    "maintainers": ["halbtonjazz"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "project_task_code",
        "portal",
    ],
    "data": [
        "templates/portal_templates.xml",
    ],
    "test": [
        "tests/test_portal.py"
    ],
}
