from odoo import fields, models, api


class ManufactureProduct(models.Model):
    """model for manufacture"""
    _name = 'manufacture.product'
    _description = "model for creating product"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'simple_product_id'

    simple_product_id = fields.Many2one('simple.product', 'product')
    bom_ids = fields.One2many('component.table', 'manufacture_id')
    quantity = fields.Integer('quantity', default=1)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'), ], string='Status', required=True, copy=False, tracking=True, default='draft')
    sale_order_id = fields.Many2one('sale.order','sale order')

    @api.onchange('simple_product_id')
    def onchange_product(self):
        """clear the components"""
        if self.bom_ids:
            self.bom_ids = self.simple_product_id.component_ids if self.simple_product_id  else  [fields.Command.clear()]
        else:
            """to get the components"""
            if self.simple_product_id:
                line = []
                for rec in self.simple_product_id.component_ids:
                    line.append(fields.Command.create({'product_id': rec.product_id, 'quantity': rec.quantity}))
                self.write({'bom_ids': line})

    @api.onchange('quantity')
    def onchange_quantity(self):
        i = 0
        for rec in self.bom_ids:
            rec.quantity = self.simple_product_id.component_ids[i].quantity * self.quantity
            i += 1

    def create_product(self):
        """to creating the product"""
        self.sale_order_id.action_confirm()
        self.state = 'confirmed'
        stock = self.env['stock.quant'].search([('product_tmpl_id', '=', self.simple_product_id.product_id.id)])
        if len(stock) == 0:
            """for adding new product in stock"""
            self.env['stock.quant'].create({
                'product_id': self.simple_product_id.product_id.product_variant_id.id,
                'quantity': self.quantity,
                'location_id': 8
            })
        else:
            """for existing product"""
            for rec in stock:
                rec.quantity += self.quantity
        for rec in self.bom_ids:
            stock_order_line = self.env['stock.quant'].search(
                [('product_tmpl_id', '=', rec.product_id.id)])
            for value in stock_order_line:
                if len(stock_order_line) > 0:
                    value.quantity = value.quantity - rec.quantity
                else:
                    pass
