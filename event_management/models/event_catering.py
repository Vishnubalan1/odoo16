# -*- coding: utf-8 -*-


from odoo import fields, models, api
from datetime import datetime


class EventCatering(models.Model):
    """ event catering model"""
    _name = "event.catering"
    _description = "caterings details"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='name', required=True,
                       readonly=True, default=lambda self: 'New')
    event_booking_id = fields.Many2one('event.booking', string='Event', required=True)
    booking_date_id = fields.Date(related='event_booking_id.booking_date', string='Booking date')
    start_date_id = fields.Datetime(related='event_booking_id.event_start_date', string='Start date')
    end_date_id = fields.Datetime(related='event_booking_id.event_end_date', string='End date')
    guests = fields.Integer('Guests')
    welcome_drink = fields.Boolean('Welcome drink')
    break_fast = fields.Boolean('Break fast')
    lunch = fields.Boolean('Lunch')
    dinner = fields.Boolean('Dinner')
    snacks_drinks = fields.Boolean('Snacks&Drinks')
    beverages = fields.Boolean('Beverages')
    welcome_drink_ids = fields.One2many('catering.table', 'welcome_drink_id')
    break_fast_ids = fields.One2many('catering.table', 'break_fast_id')
    lunch_ids = fields.One2many('catering.table', 'lunch_id')
    dinner_ids = fields.One2many('catering.table', 'dinner_id')
    snacks_drinks_ids = fields.One2many('catering.table', 'snacks_drinks_id')
    beverages_ids = fields.One2many('catering.table', 'beverages_id')
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    total_welcome_drink = fields.Monetary(string="Total", compute='compute_total_welcome', store=True)
    total_break_fast = fields.Monetary(string="Total", compute='compute_total_breakfast', store=True)
    total_lunch = fields.Monetary(string="Total",
                                  compute='compute_total_lunch', store=True)
    total_dinner = fields.Monetary(string='Total', compute='compute_total_dinner', store=True)
    total_snacks_drinks = fields.Monetary(string="Total", compute='compute_total_snacks', store=True)
    total_beverages = fields.Monetary(string='Total', compute='compute_total_beverages', store=True)
    total = fields.Monetary(string='Grand Total', compute='compute_total', store=True)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'), ], string='Status', required=True, copy=False, tracking=True, default='draft')

    def button_confirmed(self):

        self.state = "confirmed"
        self.event_booking_id.state = 'confirmed'
        print(self.event_booking_id.id)

    @api.model
    def create(self, vals):
        """ for creating sequence"""
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'event.catering') or 'New'
        return super(EventCatering, self).create(vals)

    @api.depends('welcome_drink_ids', 'welcome_drink')
    def compute_total_welcome(self):
        """compute  total of welcome drink"""

        if self.welcome_drink:
            self.write({
                'total_welcome_drink': sum(self.welcome_drink_ids.mapped('sub_total'))
            })
        else:
            self.welcome_drink_ids = [fields.Command.clear()]

    @api.depends('break_fast_ids', 'break_fast')
    def compute_total_breakfast(self):
        """compute  total of break fast"""
        if self.break_fast:
            self.write({
                'total_break_fast': sum(self.break_fast_ids.mapped('sub_total'))
            })
        else:
            self.break_fast_ids = [fields.Command.clear()]

    @api.depends('lunch_ids', 'lunch')
    def compute_total_lunch(self):
        """compute  total of lunch"""
        if self.lunch:
            self.write({
                'total_lunch': sum(self.lunch_ids.mapped('sub_total'))
            })
        else:
            self.lunch_ids = [fields.Command.clear()]

    @api.depends('dinner_ids', 'dinner')
    def compute_total_dinner(self):
        """compute  total of dinner"""
        if self.dinner:
            self.write({
                'total_dinner': sum(self.dinner_ids.mapped('sub_total'))
            })
        else:
            self.dinner_ids = [fields.Command.clear()]

    @api.depends('snacks_drinks_ids', 'snacks_drinks')
    def compute_total_snacks(self):
        """compute  total of snacks&drinks"""
        if self.snacks_drinks:
            self.write({
                'total_snacks_drinks': sum(self.snacks_drinks_ids.mapped('sub_total'))
            })
        else:
            self.snacks_drinks_ids = [fields.Command.clear()]

    @api.depends('beverages_ids', 'beverages')
    def compute_total_beverages(self):
        """compute  total of beverages"""
        if self.beverages:
            self.write({
                'total_beverages': sum(self.beverages_ids.mapped('sub_total'))
            })
        else:
            self.beverages_ids = [fields.Command.clear()]

    @api.depends('total_welcome_drink', 'total_break_fast', 'total_lunch', 'total_dinner', 'total_snacks_drinks',
                 'total_beverages')
    def compute_total(self):
        """compute  grand total"""
        self.total = 0
        for amount in self:
            amount.total = amount.total_dinner + amount.total_beverages + amount.total_lunch + amount.total_snacks_drinks + amount.total_break_fast + amount.total_welcome_drink
