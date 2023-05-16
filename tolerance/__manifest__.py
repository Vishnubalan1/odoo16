# -*- coding: utf-8 -*-

{
    'name': "tolerance for customer",
    'version': '16.1.0.0',
    'depends': ['base', 'sale', 'purchase', 'stock'],
    'author': "vishnu",
    'application': True,
    'description': """tolerance for customer""",
    'data': [
        'security/ir.model.access.csv',
        'wizard/exception_wizard_views.xml',
        'views/res_partner_views.xml',
        'views/purchase_order_views.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',

    ]

}
