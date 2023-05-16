# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SaleOrderWizard(models.TransientModel):
    """wizard for exception"""
    _name = 'exception.wizard'
    _description = "exception wizard"

    picking_id = fields.Many2one('stock.picking',string='picking')

    def accept_button(self):
        """button for accept"""

        value = self.env['stock.picking'].search([('id','=',self.picking_id.id)])

        if not value.env.context.get('button_validate_picking_ids'):
            self = value.with_context(button_validate_picking_ids=value.ids)
        self.env['stock.backorder.confirmation'].process()
        value.button_check()


