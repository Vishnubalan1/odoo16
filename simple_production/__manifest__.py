{
    'name': "simple production",
    'version': '16.1.0.0',
    'depends': ['base', 'product', 'mail', 'account','sale'],
    'author': "vishnu",
    'application': True,
    'description': """simple production""",
    'data': [
        'security/ir.model.access.csv',
        'views/manufacture_views.xml',
        'views/simple_production_views.xml',

    ]

}
