from odoo import fields, models, api, _



class PurchaseOrder(models.Model):
    """inheriting purchase.order"""
    _inherit = 'purchase.order'
    tolerance = fields.Float(string='tolerance', readonly=False, compute='get_tolerance',
                             inverse='_inverse_tolerance',
                             store=True)

    @api.depends('partner_id')
    def get_tolerance(self):
        """compute tolerance"""

        for rec in self:
            rec.tolerance = rec.partner_id.tolerance

    def _inverse_tolerance(self):
        pass
