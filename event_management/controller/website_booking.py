# -*- coding: utf-8 -*-
from datetime import date

from odoo import http
from odoo.http import request
from odoo import fields


class BookingForm(http.Controller):
    @http.route(['/event'], type='http', auth="user", website=True)
    def event_booking(self):
        event = http.request.env['event.booking'].sudo().search([])
        partner = http.request.env['res.partner'].sudo().search([])
        type = http.request.env['event.types'].sudo().search([])
        c_date = date.today()

        return request.render("event_management.online_event_booking_form", {
            'event': event,
            'partner': partner,
            'type': type,

        })

    @http.route(['/event/submit'], type='http', auth="user", website=True)
    def website_booking(self, **kwargs):
        # # print(kwargs['partner_id'])
        print(kwargs['booking_date'])
        print(date.today())
        # print(kwargs['type_id'])
        # # # print(kwargs['type'])
        #
        #
        # print('hai')
        http.request.env['event.booking'].create(kwargs)
        return request.render("event_management.complete_page")
