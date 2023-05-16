# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    """inheriting sale order model"""

    def import_order_line(self):
        """button for  wizard"""
        return {

            'name': 'import files',
            'type': 'ir.actions.act_window',
            'res_model': 'import.file.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_sale_id': self.id,
                        }
        }

