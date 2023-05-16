# -*- coding: utf-8 -*-
from odoo import fields, models


class EventTypes(models.Model):
    """ event type model"""
    _name = "event.types"
    _description = "different types of events"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('name', required=True)
    code = fields.Char('Code')
    image = fields.Image('image')


































































































































































































































































































































































































































































































































