# -*- coding: utf-8 -*-
from odoo import fields, models, api


class EventService(models.Model):
    """service model"""
    _name = "event.service"
    _description = "event services"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=True)
    responsible_person_id = fields.Many2one('res.users', string="Responsible person")
    table_ids = fields.One2many('event.table', 'service_id')
    company_id = fields.Many2one('res.company', store=True, copy=False, string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency", related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    total = fields.Monetary('Total', compute='compute_total', store=True)

    @api.depends('table_ids')
    def compute_total(self):
        self.write({
            'total': sum(self.table_ids.mapped('sub_total'))
        })
