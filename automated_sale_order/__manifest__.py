{
    'name': "automated sale order",
    'version': '16.1.0.0',
    'depends': ['base','product','sale_management','purchase'],
    'author': "vishnu",
    'application': True,
    'description': """automated sale order""",
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_wizard_views.xml','views/product_template_view.xml'
    ]

}
