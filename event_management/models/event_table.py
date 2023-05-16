# -*- coding: utf-8 -*-

from odoo import fields, models, api


class EventTable(models.Model):
    """ service table  """
    _name = "event.table"
    _description = "event table"

    description = fields.Char('Description', required=True)
    unit_prize = fields.Float('Unit prize')
    service_id = fields.Many2one(
        'event.service',
        string="new",
    )
    quantity = fields.Float('Quantity')
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    sub_total = fields.Monetary(string="Sub Total", compute='_compute_amount', store=True)

    @api.depends('unit_prize', 'quantity')
    def _compute_amount(self):
        """
        compute the subtotal of each line.
        """
        for line in self:
            line.sub_total = line.quantity * line.unit_prize
