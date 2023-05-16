# -*- coding: utf-8 -*-


from odoo import fields, models


class CateringMenu(models.Model):
    """ event catering management"""
    _name = "catering.menu"
    _description = "menus in the event"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Dish name', required=True)
    category = fields.Selection(string="Category", selection=[('welcome_drink', 'Welcome Drink'),
                                                              ('break_fast', 'Break Fast'), ('lunch', 'Lunch'),
                                                              ('dinner', 'Dinner'),
                                                              ('snacks_drinks', 'Snacks&Drinks'),
                                                              ('beverages', 'Beverages')], required=True)
    image = fields.Image('Image')
    unit_prize = fields.Float('Unit prize')
    uom_id = fields.Many2one('uom.uom', string='UOM', default=1)
