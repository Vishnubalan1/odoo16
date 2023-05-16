# -*- coding: utf-8 -*-
from odoo import fields, models, api
from datetime import datetime
from odoo.exceptions import ValidationError


class EventBooking(models.Model):
    """ event booking model"""
    _name = "event.booking"
    _description = "event booking details"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    name = fields.Char('Name', compute='_compute_name',store=True)
    invoice_id = fields.Many2one('account.move')
    event_type_id = fields.Many2one('event.types', string='Event Type', required=True)
    booking_date = fields.Date('Booking Date', default=fields.Date.today())
    event_start_date = fields.Datetime(' Start date ', required=True)
    event_end_date = fields.Datetime('End date ', required=True)
    duration = fields.Float(string=' Duration', compute='_compute_duration', store=True, readonly=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer",
        required=True, readonly=False
    )
    # sale_order_id = fields.Many2one('sale.order','sale order')
    payment_status = fields.Char(compute='compute_status', string='payment state')
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
        ('invoice', 'Invoiced'),
        ('expired', 'Expired'),

    ], string='Status', required=True, copy=False,
        tracking=True, default='draft')
    invoice_count = fields.Integer(compute='compute_count')

    def catering_service(self):
        """ button for catering form """
        return {
            'name': 'My Form',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'event.catering',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context': {'default_event_booking_id': self.id}
        }

    def button_confirmed(self):
        """ button for confirm"""
        self.write({
            'state': "confirmed",
        })

    def button_deliver(self):
        """button for deliver"""
        self.write({
            'state': "delivered",

        })
        self.env['event.catering'].search([('event_booking_id', '=', self.id)]).write({
            'state': "delivered",
        })

    @api.depends('event_start_date', 'event_end_date')
    def _compute_duration(self):
        """for creating duration of event"""
        for times in self:
            if times.event_start_date and times.event_end_date:
                if times.event_start_date > times.event_end_date:
                    raise ValidationError('add a valid end date')
                else:
                    timedelta = times.event_end_date - times.event_start_date
                    times.duration = timedelta.days

    @api.depends('event_start_date', 'event_end_date', 'event_type_id', 'partner_id')
    def _compute_name(self):
        """ for getting the name"""
        for rec in self:
            if rec.event_start_date and rec.event_end_date and rec.event_type_id and rec.partner_id:
                start = rec.event_start_date.strftime("%d-%m-%Y")
                end = rec.event_end_date.strftime("%d-%m-%Y")
                full_name = rec.partner_id.name
                all_words = full_name.split()
                first_name = all_words[0]
                rec.name = str(rec.event_type_id.name) + ':' + first_name + '/' + start + ':' + end
            else:
                rec.name = 'New'

    def scheduled_change_state(self):
        """ to change the state while start date is expired"""
        for rec in self.search([('state', '=', 'draft')]):
            if rec.event_start_date and rec.event_start_date < datetime.today():
                rec.write({'state': 'expired'})

    @api.onchange('event_start_date', 'state')
    def expire_state(self):
        """ to expire the past events"""
        for date in self:
            if date.event_start_date:
                if date.event_start_date < datetime.today():
                    date.write({'state': 'expired'})
                else:
                    date.write({'state': 'draft'})

    def get_catering(self):
        """smart button catering"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Catering',
            'view_mode': 'tree,form',
            'res_model': 'event.catering',
            'domain': [('event_booking_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def invoice_button(self):
        """creating invoice"""
        for record in self:
            values = self.env['event.catering'].search([('event_booking_id', '=', self.id)])
            invoice_line = []
            self.write({
                'state': "invoice", })

            tables = values.welcome_drink_ids + values.break_fast_ids + values.lunch_ids + values.dinner_ids + values.snacks_drinks_ids + values.beverages_ids
            for rec in tables:
                invoice_line.append(fields.Command.create({
                    'name': rec.item.name,
                    'price_unit': rec.unit_prize,
                    'quantity': rec.quantity
                }))

            invoice = self.env['account.move'].create([
                {
                    'move_type': 'out_invoice',
                    'invoice_date': fields.Date.context_today(self),
                    'partner_id': record.partner_id.id,
                    'currency_id': values.currency_id.id,
                    'invoice_line_ids': invoice_line
                }
            ])
            self.write({'invoice_id': invoice.id})
            return {
                'view_mode': 'form',
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'res_id': invoice.id,
                'context': self.env.context
            }

    def get_invoice(self):
        """smart button invoice"""

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
            'domain': [('id', '=', self.invoice_id)],
            'context': "{'create': False}"
        }

    def compute_count(self):
        """count of invoice"""
        if self.invoice_id:
            self.invoice_count = 1
        else:
            self.invoice_count = 0

    def compute_status(self):
        """for paid ribbon in invoice"""
        record = self.invoice_id.payment_state
        self.write({
            'payment_status': record
        })
