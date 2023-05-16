# -*- coding: utf-8 -*-

import datetime
from datetime import datetime
from odoo.exceptions import ValidationError
from odoo import fields, models, api, _
from odoo.tools import date_utils
import io
import json

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class ReportWizard(models.TransientModel):
    """wizard for creating  Report"""
    _name = 'report.wizard'
    _description = "wizard for reporting"

    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    type_id = fields.Many2one('event.types', 'Event Type')
    catering = fields.Boolean('Include Catering')
    date = fields.Date('current date', default=datetime.today())
    partner_id = fields.Many2one("res.partner", 'Customer')

    def print_report(self):
        """button to print the wizard"""
        if self.catering:
            query_1 = f" ,catering_menu.name,catering_table.quantity," \
                      f"catering_table.unit_prize,catering_table.sub_total,event_catering.total"
            query_2 = f" INNER JOIN event_catering ON event_catering.event_booking_id = event_booking.id INNER JOIN " \
                      f"catering_table ON catering_table.welcome_drink_id = event_catering.id or " \
                      f"catering_table.break_fast_id = event_catering.id or catering_table.lunch_id = event_catering.id or " \
                      f"catering_table.dinner_id = event_catering.id or catering_table.snacks_drinks_id = event_catering.id " \
                      f"INNER JOIN catering_menu  ON catering_menu.id = catering_table.item "
        else:
            query_1 = " "
            query_2 = " "
        main_query = "select event_booking.name as booking,event_booking.booking_date, event_booking.state, " \
                     "event_types.name " \
                     "as type,res_partner.name as customer" + query_1 + " from event_booking " + "INNER JOIN event_types ON " \
                                                                                                 "event_booking.event_type_id =event_types.id INNER JOIN res_partner ON event_booking.partner_id " \
                                                                                                 "= res_partner.id" + query_2
        if self.from_date and self.to_date:
            if self.from_date > self.to_date:
                raise ValidationError('date not valid')

        if self.type_id:
            """report type wise"""
            query = f"and event_booking.event_type_id={self.type_id.id} "
            main_query = main_query + query
        if self.partner_id:
            """report customer wise"""
            query = f"and event_booking.partner_id={self.partner_id.id} "
            main_query = main_query + query

        if self.from_date and self.to_date:
            """report between dates"""
            main_query += f" and event_booking.booking_date  BETWEEN '{self.from_date}' and '{self.to_date}'"

        elif self.from_date:
            """report where only from date is given"""
            main_query += f" and event_booking.booking_date >='{self.from_date}'"
        elif self.to_date:
            """report where only to date is given"""
            main_query += f" and event_booking.booking_date <='{self.to_date}'"
        self.env.cr.execute(main_query)
        record = self.env.cr.dictfetchall()

        data = {
            'model_id': self.id,
            'to_date': self.to_date,
            'from_date': self.from_date,
            'event_type': self.type_id.name,
            'date': self.date,
            'record': record,
            'catering': self.catering,

        }
        if not record:
            raise ValidationError('There is no record')
        return self.env.ref('event_management.action_report_event_management').report_action(None, data=data)

    def print_xl_report(self):
        if self.from_date and self.to_date:
            if self.from_date > self.to_date:
                raise ValidationError('date not valid')

        if self.catering:
            var_1 = f" ,catering_menu.name,catering_table.quantity," \
                    f"catering_table.unit_prize,catering_table.sub_total,event_catering.total,catering_table.break_fast_id,catering_table.welcome_drink_id,catering_table.lunch_id ,catering_table.dinner_id ,catering_table.snacks_drinks_id,event_catering.id"
            var_2 = f" INNER JOIN event_catering ON event_catering.event_booking_id = event_booking.id INNER JOIN " \
                    f"catering_table ON catering_table.welcome_drink_id = event_catering.id or " \
                    f"catering_table.break_fast_id = event_catering.id or catering_table.lunch_id = event_catering.id or " \
                    f"catering_table.dinner_id = event_catering.id or catering_table.snacks_drinks_id = event_catering.id " \
                    f"INNER JOIN catering_menu  ON catering_menu.id = catering_table.item "
        else:
            var_1 = " "
            var_2 = " "
        main_query = "select event_booking.name as booking,event_booking.booking_date, event_booking.state, " \
                     "event_types.name " \
                     "as type,res_partner.name as customer" + var_1 + " from event_booking " + "INNER JOIN event_types ON " \
                                                                                               "event_booking.event_type_id =event_types.id INNER JOIN res_partner ON event_booking.partner_id " \
                                                                                               "= res_partner.id" + var_2
        if self.from_date and self.to_date:
            if self.from_date > self.to_date:
                raise ValidationError('date not valid')

        if self.type_id:
            """report type wise"""
            query = f"and event_booking.event_type_id={self.type_id.id} "
            main_query = main_query + query
        if self.partner_id:
            """report customer wise"""
            query = f"and event_booking.partner_id={self.partner_id.id} "
            main_query = main_query + query

        if self.from_date and self.to_date:
            """report between dates"""
            main_query += f" and event_booking.booking_date  BETWEEN '{self.from_date}' and '{self.to_date}'"

        elif self.from_date:
            """report where only from date is given"""
            main_query += f" and event_booking.booking_date >='{self.from_date}'"
        elif self.to_date:
            """report where only to date is given"""
            main_query += f" and event_booking.booking_date <='{self.to_date}'"
        self.env.cr.execute(main_query)
        record = self.env.cr.dictfetchall()
        data = {
            'model_id': self.id,
            'to_date': self.to_date,
            'from_date': self.from_date,
            'event_type': self.type_id.name,
            'date': self.date,
            'record': record,
            'catering': self.catering,

        }

        return {
            'type': 'ir.actions.report',
            'data': {'model': 'report.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        from_date = data['from_date']
        to_date = data['to_date']
        catering = data['catering']
        record = data['record']
        date = data['date']
        # print(catering)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()

        cell_format = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '12px'})
        cell_format_1 = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '8px'})

        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '12px', 'align': 'center'})
        txt_1 = workbook.add_format(
            {'align': 'center', 'font_size': '8px'})

        sheet.merge_range('G2:M3', 'EVENT MANAGEMENT REPORT', head)
        sheet.write('A9', 'SL NO', cell_format)
        sheet.merge_range('B9:F9', 'EVENT NAME', cell_format)
        sheet.merge_range('I9:K9', 'CUSTOMER NAME', cell_format)
        sheet.merge_range('L9:M9', 'BOOKING DATE', cell_format)
        sheet.merge_range('G9:H9', 'STATUS', cell_format)
        if not data['event_type']:
            sheet.merge_range('N9:O9', 'EVENT TYPE', cell_format)
        else:
            sheet.merge_range('A7:B7', data['event_type'], cell_format)
        if from_date:
                sheet.merge_range('A6:B6', 'From Date:', cell_format)
                sheet.merge_range('C6:D6', from_date, txt)
        if to_date:
            sheet.merge_range('E6:F6', 'To Date:', cell_format)
            sheet.merge_range('G6:H6', to_date, txt)
        if not to_date or not from_date:
            sheet.merge_range('A6:B6', 'Current Date:', cell_format)
            sheet.merge_range('C6:D6', date, txt)

        row = 9
        no = 1
        booking_list = []

        for i in record:

            if i['booking'] not in booking_list:
                booking_list.append(i['booking'])
                sheet.write('A' + str(row + 1), no, txt)
                sheet.merge_range('B' + str(row + 1) + ':F' + str(row + 1), i['booking'], txt)
                sheet.merge_range('I' + str(row + 1) + ':K' + str(row + 1), i['customer'], txt)
                sheet.merge_range('L' + str(row + 1) + ':M' + str(row + 1), i['booking_date'], txt)
                sheet.merge_range('G' + str(row + 1) + ':H' + str(row + 1), i['state'], txt)
                if not data['event_type']:
                    sheet.merge_range('N' + str(row + 1) + ':O' + str(row + 1), i['type'], txt)
                h = row + 1

                if catering:
                    sheet.merge_range('B' + str(h + 1) + ':F' + str(h + 1), 'Catering item', cell_format_1)
                    sheet.merge_range('G' + str(h + 1) + ':H' + str(h + 1), 'Quantity', cell_format_1)
                    sheet.merge_range('I' + str(h + 1) + ':K' + str(h + 1), 'Unit  prize', cell_format_1)
                    sheet.merge_range('L' + str(h + 1) + ':M' + str(h + 1), 'Sub total', cell_format_1)
                    sheet.merge_range('N' + str(h + 1) + ':O' + str(h + 1), 'Total', cell_format_1)
                    total = 0

                    for j in record:
                        if i['id'] == j['welcome_drink_id'] or i['id'] == j['break_fast_id'] or i['id'] == j['lunch_id']:
                            h = h +1
                            sheet.merge_range('B' + str(h + 1) + ':F' + str(h + 1), j['name'], txt_1)
                            sheet.merge_range('G' + str(h + 1) + ':H' + str(h + 1), j['quantity'], txt_1)
                            sheet.merge_range('I' + str(h + 1) + ':K' + str(h + 1), j['unit_prize'], txt_1)
                            sheet.merge_range('L' + str(h + 1) + ':M' + str(h + 1), j['sub_total'], txt_1)

                            if total == 0:
                                sheet.merge_range('N' + str(h + 1) + ':O' + str(h + 1), i['total'], txt_1)
                            total += i['total']

                no += 1
                row =h+ 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
