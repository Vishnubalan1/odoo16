from odoo import fields, models, api, _


class StockPicking(models.Model):
    """in heriting stock.picking"""
    _inherit = 'stock.picking'
    tolerance = fields.Float(string='tolerance', readonly=False, compute='get_tolerance', inverse='_inverse_tolerance',
                             store=True)

    @api.depends('partner_id')
    def get_tolerance(self):
        """compute tolerance"""

        for rec in self:
            rec.tolerance = rec.partner_id.tolerance

    def _inverse_tolerance(self):
        pass

    def button_check(self):
        """validation button"""
        move_line = self.move_line_ids
        if not self.env.context.get('button_validate_picking_ids'):
            self = self.with_context(button_validate_picking_ids=self.ids)

        for rec in move_line:
            ordered = int(rec.move_id.product_uom_qty)
            record = int(rec.move_id.product_uom_qty + self.tolerance)
            value = int(rec.move_id.product_uom_qty - self.tolerance)
            done = int(rec.move_id.quantity_done)

            if done < ordered:
                if done not in range(value, record + 1):
                    """returning wizard"""
                    return {
                        'name': 'check it',
                        'type': 'ir.actions.act_window',
                        'res_model': 'exception.wizard',
                        'view_mode': 'form',
                        'target': 'new',
                        'context': {'default_picking_id': self.id}
                    }
                else:
                    """returning wizard"""
                    view = self.env.ref('stock.view_backorder_confirmation')
                    print(self.id)
                    return {
                        'name': _('Create Backorder?'),
                        'type': 'ir.actions.act_window',
                        'view_mode': 'form',
                        'res_model': 'stock.backorder.confirmation',
                        'views': [(view.id, 'form')],
                        'view_id': view.id,
                        'target': 'new',
                        'context': dict(self.env.context, default_show_transfers=False,
                                        default_pick_ids=[(4, p.id) for p in self])}

            elif done not in range(value, record + 1):
                """returning wizard"""
                return {
                    'name': 'check it',
                    'type': 'ir.actions.act_window',
                    'res_model': 'exception.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {'default_picking_id': self.id}
                }
            else:
                self.button_validate()
