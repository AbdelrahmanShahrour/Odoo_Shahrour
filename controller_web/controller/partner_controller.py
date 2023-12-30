from odoo.http import request
from odoo import http
import json

class PartnerController(http.Controller):
    '''
    This controller is responsible for handling requests related to partner data.
    - GET /api/partner    (read) --not implemented
    - POST /api/partner (create)  --done
    - PUT /api/partner    (update) --not implemented
    - DELETE /api/partner (delete) --not implemented

    this endpoint '/partner_form' is responsible for rendering the form
    - GET /partner_form
    -- render the form
    this endpoint '/create_partner' is responsible for creating a new partner
    - POST /create_partner
    -- create a new partner
    '''
    @http.route('/partner_form', auth='public', type='http', methods=['GET'], website=True)
    def partner_form(self, **kwargs):
        return request.render("controller_web.partner_form_template")

    @http.route('/create_partner', auth='public', type='http', methods=['POST'], website=True, csrf=False)
    def create_partner(self, **post):
        # Create partner
        Partner = request.env['res.partner'].sudo()
        partner_data = {
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
        }
        existing_partner = Partner.search([('email', '=', post.get('email'))])

        if existing_partner:
            response = {
                'error': 'A partner with this email already exists.'
            }
            return request.make_response(json.dumps(response), [('Content-Type', 'application/json')])

        partner = Partner.create(partner_data)
        return "Partner created successfully! ID: {}".format(partner.id)
