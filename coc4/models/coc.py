# -*- coding: utf-8 -*-

from odoo import fields, models


class CoC(models.Model):
    _name = 'clash.codes'
    _description = 'new model' \
                   ''
    """coc model"""

    resistence = fields.Selection([('pass', 'Pass'), ('fail', 'Fail')])


