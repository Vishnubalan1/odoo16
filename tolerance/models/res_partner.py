from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    """for adding tolerance field inheriting res_partner"""
    _inherit = 'res.partner'
    tolerance = fields.Float('Tolerance %')
