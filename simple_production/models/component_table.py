from odoo import fields, models, api


class ComponentTable(models.Model):
    """ component table  """
    _name = "component.table"
    _description = "table for components"

    product_id = fields.Many2one('product.template', string='components')
    description = fields.Char('Description')
    quantity = fields.Float('quantity')
    production_id = fields.Many2one(
        'simple.product',
        string="simple production",
    )
    manufacture_id = fields.Many2one(
        'manufacture.product',
        string="simple production",
    )

    @api.onchange('product_id')
    def onchange_quantity(self):
        if self.product_id:
            self.quantity = 1
        else:
            self.quantity = 0
