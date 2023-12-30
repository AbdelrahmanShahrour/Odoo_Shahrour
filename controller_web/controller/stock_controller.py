from odoo.http import request
from odoo import http
import json

class StockController(http.Controller):
    '''
    This controller is responsible for handling requests related to stock data.
    - GET /api/stock    (read) --done
    - POST /api/stock (create)  --not implemented
    - PUT /api/stock    (update) --not implemented
    - DELETE /api/stock (delete) --not implemented
    '''
    @http.route('/api/stock', auth='user', type='http', methods=['GET'])
    def get_stock_data(self, **kwargs):
        Quant = http.request.env['stock.quant']
        quants = Quant.search([])
        stock_data = []

        for quant in quants:
            stock_data.append({
                'product_id': quant.product_id.id,
                'product_name': quant.product_id.name,
                'quantity': quant.quantity,
                'location_id': quant.location_id.id,
                'location_name': quant.location_id.name
            })

        return http.request.render('controller_web.stock_list_template', {'stock_data': stock_data})