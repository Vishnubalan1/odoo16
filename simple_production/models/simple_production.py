# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SimpleProduction(models.Model):
    """model for bom"""
    _name = 'simple.product'
    _description = "model for creating product"
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.template', 'product',required=True)
    component_ids = fields.One2many('component.table', 'production_id',required=True)


