# -*- coding: utf-8 -*-

from odoo import fields, models, api


class CateringTable(models.Model):
    """ catering order table  """
    _name = "catering.table"
    _description = "table for catering details"
    _rec_name = 'item'

    item = fields.Many2one('catering.menu', string='Item')
    description = fields.Char('Description')
    unit_prize = fields.Float(string='Unit prize', readonly=False,compute='compute_unit_prize',inverse='_inverse_unit_prize' , store=True)
    uom_id = fields.Many2one(related='item.uom_id', string='UOM', readonly=False)
    welcome_drink_id = fields.Many2one(
        'event.catering',
        string="welcome drinks",
    )
    break_fast_id = fields.Many2one(
        'event.catering',
        string="break fast",
    )
    lunch_id = fields.Many2one(
        'event.catering',
        string="lunch",
    )
    dinner_id = fields.Many2one(
        'event.catering',
        string="dinner",
    )
    snacks_drinks_id = fields.Many2one(
        'event.catering',
        string="snacks&drinks",
    )
    beverages_id = fields.Many2one(
        'event.catering',
        string="beverage",
    )
    quantity = fields.Float('Quantity', default='1')

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

    @api.depends('item')
    def compute_unit_prize(self):
        """compute unit prize"""
        for rec in self:
            rec.unit_prize = rec.item.unit_prize

    def _inverse_unit_prize(self):
        pass
