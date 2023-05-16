# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SaleOrder(models.Model):
    """inheriting sale.order model"""
    _inherit = 'sale.order'

    def multiple_invoice(self):
        """for getting wizard"""
        self.env['invoice.wizard'].create({
        })
        return {

            'name': 'choose invoices',
            'type': 'ir.actions.act_window',
            'res_model': 'invoice.wizard',
            'view_mode': 'form',
            'target': 'new',

        }



