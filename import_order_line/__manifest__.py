# -*- coding: utf-8 -*-
{
    'name': "import_order_line",
    'version': '16.0.1.0.0',
    'depends': ['base', 'sale'],
    'author': "vishnu",
    'category': 'order line',
    'application': True,
    'description': """ module for importing order lines""",
    'data': ['security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'wizard/import_file_wizard.xml'
    ]
}
