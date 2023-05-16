# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    """inheriting product template model"""

    def sale_order(self):
        """button for sale wizard"""
        self.env['sale.order.wizard'].create({
        })
        return {

            'name': 'Sale order',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_price': self.list_price,
                        'default_product_id': self.id,
                        "default_name": self.name,
                        "default_value": "one"
                        }
        }

    def purchase(self):
        """button for purchase wizard"""
        self.env['sale.order.wizard'].create({

        })
        self.env['sale.order.wizard'].value = 'two'

        return {

            'name': 'Purchase order',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_price': self.list_price,
                        'default_product_id': self.id,
                        "default_name": self.name,
                        "default_value": "two"
                        }
        }
