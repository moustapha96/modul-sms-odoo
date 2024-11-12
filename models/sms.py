from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests

class SmsConfig(models.Model):
    _name = 'sms.config'
    _description = 'SMS Configuration'

    api_key = fields.Char('API Key')
    api_secret = fields.Char('API Secret')
    sender_id = fields.Char('Sender ID')

    @api.model
    def get_default_config(self):
        config = self.search([], limit=1)
        return config if config else False

class SendSms(models.Model):
    _name = 'send.sms'
    _description = 'Send SMS'

    recipient = fields.Char('Recipient', required=True)
    message = fields.Text('Message', required=True)
    status = fields.Selection(
        [
            ('pending', 'En attente'),
            ('sent', 'Envoyé'),
            ('failed', 'Echec'),
        ],
        string='Statut',
        default='pending',
    )

    @api.multi
    def send_sms(self):
        config = self.env['sms.config'].get_default_config()
        if not config:
            raise UserError("Please configure SMS settings first!")

        try:
            # Composez l'URL de l'API Orange Sonatel
            api_url = "https://api.orange.com/smsmessaging/v1/outbound/tel:+221" + config.sender_id + "/requests"
            headers = {
                'Authorization': self.env['ir.config_parameter'].sudo().get_param('my_orange_sms_module.sms_token'),
                'Content-Type': 'application/json'
            }
            data = {
                'outboundSMSMessageRequest': {
                    'address': 'tel:+221' + self.recipient,
                    'outboundSMSTextMessage': {
                        'message': self.message
                    },
                    'senderAddress': 'tel:+221' + config.sender_id,
                    'senderName': 'CCBM SHOP',
                }
            }

            response = requests.post(api_url, headers=headers, json=data)

            if response.status_code == 200:
                self.status = 'sent'
                self.message = "SMS sent successfully!"
            elif response.status_code == 401:
                self.status = 'failed'
                self.message = "Error sending SMS: Unauthorized"
            else:
                self.status = 'failed'
                self.message = "Error sending SMS: " + response.text
        except Exception as e:
            self.status = 'failed'
            self.message = "Error sending SMS: " + str(e)

        return True

class SmsHistory(models.Model):
    _name = 'sms.history'
    _description = 'SMS History'

    recipient = fields.Char('Recipient')
    message = fields.Text('Message')
    status = fields.Selection(
        [
            ('pending', 'En attente'),
            ('sent', 'Envoyé'),
            ('failed', 'Echec'),
        ],
        string='Statut',
        default='pending',
    )
    send_date = fields.Datetime('Date d\'envoi', default=fields.Datetime.now)

class SmsModel(models.Model):
    _name = 'sms.model'
    _description = 'SMS Model'

    code = fields.Char('Code', required=True)
    message = fields.Text('Message', required=True)
    parametre = fields.Char('Paramètre', required=True)

    @api.onchange('parametre')
    def onchange_parametre(self):
        self.message = self.message.replace("]","").replace("[","")


