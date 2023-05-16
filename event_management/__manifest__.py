# -*- coding: utf-8 -*-
{
    'name': "event_management",
    'version': '16.0.1.0.0',
    'depends': ['base','mail','sale','account','website'],
    'author': "vishnu",
    'category': 'Event Management',
    'application': True,
    'description': """ module for event_management configuration""",
    'data': [
        'data/data_demo.xml',
        'data/ir_cron.xml',
        'data/ir.sequence.xml',
        'security/ir.model.access.csv',
        'views/event_services.xml',
        'views/event_booking.xml',
        'views/event_catering.xml',
        'views/catering_menu.xml',
        'views/event_types.xml',
        'wizard/reporting_wizard.xml',
        'reports/event_report.xml',
        'views/tmp_event_website.xml',
        'views/complete_website.xml',
        'reports/event_report_template.xml',
        'views/tmp_event_website.xml',
        'views/event_menus.xml',
        'views/event_website.xml'
    ],
    'assets': {
        'web.assets_backend' : [
            'event_management/static/src/js/action_report.js',
        ],}
}
