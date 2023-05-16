# -*- coding: utf-8 -*-

{
    'name': "multiple sale order invoices ",
    'version': '16.1.0.0',
    'depends': ['base', 'sale', 'account'],
    'author': "vishnu",
    'application': True,
    'description': """multiple sale order invoices""",
    'data': [
        'views/inoice_wizard.xml',
        'views/sale_order_views.xml',
        'security/ir.model.access.csv'
    ]

}
