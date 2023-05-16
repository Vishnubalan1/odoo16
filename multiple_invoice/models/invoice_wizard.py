# -*- coding: utf-8 -*-

from odoo import fields, models, api


class InvoiceWizard(models.TransientModel):
    """wizard for creating  multiple invoices"""
    _name = 'invoice.wizard'
    _description = "wizard for creating multiple invoices"

    partner_id = fields.Many2one(
        'res.partner',
        "Customer",
        required=True, readonly=False
    )
    sale_order_ids = fields.Many2many('sale.order', string='Sale Orders')
    invoice_id = fields.Many2one('account.move')

    def create_invoice(self):
        """button to create multiple invoices"""
        if self.sale_order_ids:
            for rec in self:
                invoice_line = []
                for value in rec.sale_order_ids:
                    for record in value.order_line:
                        invoice_line.append(fields.Command.create({
                            'name': record.name,
                            'price_unit': record.price_unit,
                            'quantity': record.product_uom_qty,
                            'product_id': record.product_id.id
                        }))
                source_doc = [i.name for i in rec.sale_order_ids]
                print(source_doc)
                invoice = self.env['account.move'].create([
                    {
                        'move_type': 'out_invoice',
                        'invoice_date': fields.Date.context_today(self),
                        'partner_id': value.partner_id.id,
                        'currency_id': value.currency_id.id,
                        'invoice_line_ids': invoice_line,
                        'invoice_origin': ",".join(source_doc)
                    }

                ])
                self.write({
                    'invoice_id': invoice.id
                })
                return {
                    'view_mode': 'form',
                    'type': 'ir.actions.act_window',
                    'res_model': 'account.move',
                    'res_id': invoice.id,
                    'context': self.env.context
                }


class AccountMove(models.Model):
    """inheriting account.move model"""
    _inherit = 'account.move'

    def action_register_payment(self):
        """"for changing the state"""

        res = super(AccountMove, self).action_register_payment()
        doc_list = self.invoice_origin.split(',')
        values = self.env['sale.order'].search([('name', 'in', doc_list)])
        for record in values:
            record.write({
                'invoice_status': 'invoiced'
            })
        return res
