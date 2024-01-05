from odoo import models, fields, api,_
import warnings
import logging
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    quantity_replenish = fields.Float(string="Quantity Replenish")


    def select_all_moves(self):
        for move in self.move_raw_ids:
            move.select_item = True

    def deselect_all_moves(self):
        for move in self.move_raw_ids:
            move.select_item = False

    def check_replenishment(self):
        for line in self.move_raw_ids:
            if line.select_item:

                if line.quantity_replenish != 0:
                    my_qty = line.quantity_replenish
                elif self.quantity_replenish != 0:
                    my_qty = self.quantity_replenish
                else:
                    my_qty = 0

                if my_qty == 0:
                    raise UserError(_('Please enter a quantity to replenish'))
                else:
                    line.select_item = False
                    action = self.env['product.replenish'].with_context(
                        default_product_tmpl_id=line.product_id.product_tmpl_id.id).create({
                        'product_id': line.product_id.id,
                        'product_uom_id': line.product_uom.id,
                        'quantity': my_qty,
                    })
                    action.launch_replenishment()


    processed_lines = fields.Many2many('stock.move', string='Processed Lines')

    show_replenish = fields.Boolean(string="Show Replenish", default=False, compute='compute_show_replenish')
    def compute_show_replenish(self):
        for rec in self:
            for line in rec.move_raw_ids:
                if line.select_item:
                    rec.show_replenish = True
                    break
                else:
                    rec.show_replenish = False


class StockMove(models.Model):
    _inherit = 'stock.move'

    select_item = fields.Boolean(string="Select", default=False)
    quantity_replenish = fields.Float(string="Quantity Replenish")
