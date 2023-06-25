from odoo import models, api, _

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    @api.onchange('lot_id')
    def onchange_lot_id(self):
        if self.picking_id.picking_type_id.code in ['outgoing','internal']:
            if self.product_id.tracking == 'serial':
                if len(self.env['stock.quant'].search([('lot_id','=',self.lot_id.id)])) > 0:
                    #Si no se cumple al condición anterior se ha registrado el lot pero no está en ninguna ubicación
                    lot_location = self.env['lot.location.report'].browse(self.lot_id.id)
                    if lot_location.posible_current_location:
                        return {'warning':
                                    {'title': _("Warning! Incorrect product movement"),
                                     'message': _( "The product is located in two locations: %s, %s" % (lot_location.current_location.name,lot_location.posible_current_location.name))}
                                }
                    if lot_location.current_location != self.picking_id.location_id:
                        return {'warning':
                                    {'title': _("Warning! Incorrect product movement"),
                                     'message': _( "The product is going to be moved from %s but it is located in %s." % (self.picking_id.location_id.name,lot_location.current_location.name))}
                                }