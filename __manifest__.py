{
    'name': 'Orange Sonatel SMS',
    'version': '1.0',
    'author': 'Your Name',
    'category': 'Tools',
    'summary': 'Send SMS with Orange Sonatel API',
    'description': 'This module allows you to send SMS messages from Odoo using the Orange Sonatel API.',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/sms_config_view.xml',
        'views/sms_send_view.xml',
        'views/sms_history_view.xml',
        'views/sms_model_view.xml',
    ],
    'installable': True,
    'application': True,
}
