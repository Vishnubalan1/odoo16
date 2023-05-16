from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate details"



    name = fields.Char('name', required=True)
    title = fields.Text('description')
    postcode = fields.Char('postcode')
    date_availability = fields.Date('available date')
    expected_price = fields.Float('expected price', required=True)
    selling_price = fields.Float('selling price', readonly = True, )
    bedrooms = fields.Integer('no.of bedrooms')
    living_area = fields.Integer('living area')
    facades = fields.Integer('facades')
    garage = fields.Boolean('garage')
    garden = fields.Boolean('garden')
    garden_area = fields.Integer('area of the garden')
    garden_orientation = fields.Selection(string = 'orientation of garden', selection = [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])

