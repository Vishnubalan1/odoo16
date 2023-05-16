# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
import openpyxl
import base64
from io import BytesIO
from odoo.exceptions import UserError


class SaleOrderWizard(models.TransientModel):
    """wizard for importing file"""
    _name = 'import.file.wizard'
    _description = "wizard for importing file"

    file = fields.Binary(string="Attachment", required=True)

    # file_name = fields.Char("File Name")
    sale_id = fields.Many2one('sale.order', 'sale_id')
    product_id = fields.Many2one('product.template', 'product')

    def file_import(self):
        """for adding orderliness corresponding files"""
        wb = openpyxl.load_workbook(
            filename=BytesIO(base64.b64decode(self.file)), read_only=True
        )
        ws = wb.active
        for record in ws.iter_rows(min_row=2, max_row=None, min_col=None,
                                   max_col=None, values_only=True):
            value = self.env['sale.order'].search([('id', '=', self.sale_id.id)])
            product_product = self.env['product.product'].search([('name', '=', record[0])])
            uom_id = self.env['uom.uom'].search([('name', '=', record[4])])
            print(uom_id,':',product_product)

            if product_product:
                """with existing products"""
                # print(product_product)
                value.write({
                    'order_line': [fields.Command.create({
                        'order_id': value.id,
                        'name': record[1],
                        'price_unit': record[3],
                        'product_uom_qty': record[2],
                        'product_uom': uom_id.id,
                        'product_id': product_product.id,
                    })]
                })
            else:
                """with new products"""

                product = self.env['product.product'].create({
                    'name': record[0],
                    'lst_price': record[3],
                    'uom_id': uom_id.id,
                    'uom_po_id': uom_id.id
                })
                value.write({
                    'order_line': [fields.Command.create({
                        'order_id': value.id,
                        'name': record[1],
                        'price_unit': record[3],
                        'product_uom_qty': record[2],
                        'product_uom': uom_id.id,
                        'product_id': product.id,
                    })]
                })
