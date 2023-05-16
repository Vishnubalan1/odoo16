# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SaleOrderWizard(models.TransientModel):
    """wizard for sale order"""
    _name = 'sale.order.wizard'
    _description = "wizard for creating auto sale order"

    price = fields.Float(string='prize', readonly=False)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer",
        required=True, readonly=False
    )
    quantity = fields.Float('Quantity', default='1')
    product_id = fields.Many2one('product.template')
    name = fields.Char(related='product_id.product_variant_id.name', string='name')
    value = fields.Char(default='two')

    def confirm_button(self):
        """"button for confirm sale and purchase order"""
        if self.value == 'one':
            data = self.env['sale.order'].search([('partner_id', '=', self.partner_id.id), ('state', '=', 'draft')])
            product_product = self.env['product.product'].search([('product_tmpl_id', '=', self.product_id.id)])
            if data:
                """for existing open quotation"""
                data[-1].write({
                    'order_line': [fields.Command.create({
                        'order_id': self.id,
                        'name': self.name,
                        'price_unit': self.price,
                        'product_uom_qty': self.quantity,
                        'product_id': product_product.id,

                    })],
                })
                data[-1].action_quotation_sent()
                data[-1].action_confirm()

                return {
                    'view_mode': 'form',
                    'view_type': 'form',
                    'res_model': 'sale.order',
                    'type': 'ir.actions.act_window',
                    'res_id': data[-1].id,
                    'context': self.env.context
                }

            else:
                """for new quotation """
                wizard = self.env['sale.order'].create({
                    'date_order': fields.Date.context_today(self),
                    'partner_id': self.partner_id.id,
                    'user_id': self.partner_id.user_id.id,
                    'order_line': [fields.Command.create({
                        'order_id': self.id,
                        'name': self.name,
                        'price_unit': self.price,
                        'product_uom_qty': self.quantity,
                        'product_id': product_product.id,
                    })],
                })
                wizard.action_quotation_sent()
                wizard.action_confirm()
                return {
                    'view_mode': 'form',
                    'view_type': 'form',
                    'res_model': 'sale.order',
                    'res_id': wizard.id,
                    'type': 'ir.actions.act_window',
                    'context': self.env.context
                }
        else:
            """ for purchase order"""
            data = self.env['purchase.order'].search([('partner_id', '=', self.partner_id.id), ('state', '=', 'draft')])
            product_product = self.env['product.product'].search([('product_tmpl_id', '=', self.product_id.id)])
            if data:
                """for existing open rfq"""
                data[-1].write({
                    'order_line': [fields.Command.create({
                        'order_id': self.id,
                        'name': self.name,
                        'price_unit': self.price,
                        'product_uom_qty': self.quantity,
                        'product_id': product_product.id,
                    })],
                })
                data[-1].button_confirm()
                return {
                    'view_mode': 'form',
                    'view_type': 'form',
                    'res_model': 'purchase.order',
                    'type': 'ir.actions.act_window',
                    'res_id': data[-1].id,
                    'context': self.env.context
                }
            else:
                """for new rfq """
                print(self.value)
                wizard = self.env['purchase.order'].create({
                    'date_order': fields.Date.context_today(self),
                    'partner_id': self.partner_id.id,
                    'user_id': self.partner_id.user_id.id,
                    'order_line': [fields.Command.create({
                        'order_id': self.id,
                        'name': self.name,
                        'price_unit': self.price,
                        'product_uom_qty': self.quantity,
                        'product_id': product_product.id,
                    })],
                })
                wizard.button_confirm()
                return {
                    'view_mode': 'form',
                    'view_type': 'form',
                    'res_model': 'purchase.order',
                    'res_id': wizard.id,
                    'type': 'ir.actions.act_window',
                    'context': self.env.context
                }
