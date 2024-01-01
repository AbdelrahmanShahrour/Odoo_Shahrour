from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class stock_picking(models.Model):
    _inherit = 'stock.picking'
    _description = 'stock_picking'

    def check_all_action(self):
        print("check_all_action")
        # Logic to select all products

    def uncheck_all_action(self):
        print("uncheck_all_action")
        # Logic to unselect all products

    def split_action(self):
        print("split_action")
        # Logic to split the picking

    def extract_action(self):
        print("extract_action")
        # Logic to extract the picking


class PickingSplitWizard(models.TransientModel):
    _name = 'picking.split.wizard'
    _description = 'Picking Split Wizard'

    split_option = fields.Selection([('new', 'New'), ('existing', 'Existing')], string='Split Option')
    new_picking_id = fields.Many2one('stock.picking', string='New Picking')
    existing_picking_id = fields.Many2one('stock.picking', string='Existing Picking')

    def split_picking(self):
        print("split_picking")
        # Logic to split the picking

