from odoo import api, fields, models

class TestOrangeSMS(models.Model):
    _name = 'test.orange.sms'
    _description = 'Test Orange SMS'

    recipient = fields.Char('Recipient', required=True)
    message = fields.Text('Message', required=True)

    @api.multi
    def send_sms(self):
        self.env['send.sms'].create({
            'recipient': self.recipient,
            'message': self.message,
        }).send_sms()
