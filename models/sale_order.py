from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_send_message(self):
        self.ensure_one()
        message = self.env['sale.order.message'].create({
            'name': f"Message pour la commande {self.name}",
            'message': f"Détails de la commande #{self.name}:\n\n"
                       f"Produits: {', '.join(line.product_id.name for line in self.order_line)}\n"
                       f"Montant total: {self.amount_total} {self.currency_id.symbol}",
            'sale_order_id': self.id
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Envoyer le message',
            'res_model': 'sale.order.message',
            'view_mode': 'form',
            'res_id': message.id,
            'target': 'new',
        }
