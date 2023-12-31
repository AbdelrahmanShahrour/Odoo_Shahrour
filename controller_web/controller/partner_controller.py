from odoo.http import request
from odoo import http
import json

class PartnerController(http.Controller):
    '''
    This controller is responsible for handling requests related to partner data.
    - GET /api/get_partner    (read) --done
    - POST /api/add_partner (create)  --done
    - PUT /api/update_partner    (update) --done
    - DELETE /api/delete_partner (delete) --done

    this endpoint '/partner_form' is responsible for rendering the form
    - GET /partner_form
    -- render the form
    this endpoint '/add_partner' is responsible for creating a new partner
    - POST /create_partner
    -- create a new partner

    this endpoint '/api/read_partner' is responsible for returning the partner data
    - GET /api/create_partner
    -- return the partner data

    this endpoint '/api/update_partner' is responsible for updating the partner data
    - PUT /api/update_partner
    -- update the partner data

    this endpoint '/api/delete_partner' is responsible for deleting the partner data
    - DELETE /api/delete_partner
    -- delete the partner data
    '''
    @http.route('/partner_form', auth='public', type='http', methods=['GET'], website=True)
    def partner_form(self, **kwargs):
        return request.render("controller_web.partner_form_template")

    @http.route('/api/add_partner', auth='public', type='http', methods=['POST'], website=True, csrf=False)
    def create_partner(self, **post):
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

    @http.route('/api/create_partner', auth='public', type='http', methods=['GET'], website=True, csrf=False)
    def get_partner_data(self, **kwargs):
        Partner = http.request.env['res.partner']
        partners = Partner.search([])
        partner_data = []

        for partner in partners:
            partner_data.append({
                'id': partner.id,
                'name': partner.name,
                'email': partner.email,
                'phone': partner.phone,
            })

        return http.request.make_response(json.dumps(partner_data), [('Content-Type', 'application/json')])

    @http.route('/api/update_partner', auth='public', type='http', methods=['PUT'], website=True, csrf=False)
    def update_partner(self, **post):
        Partner = http.request.env['res.partner']
        partner = Partner.search([('id', '=', post.get('id'))])
        partner.write({
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
        })
        return "Partner updated successfully! ID: {}".format(partner.id)

    @http.route('/api/delete_partner', auth='public', type='http', methods=['DELETE'], website=True, csrf=False)
    def delete_partner(self, **post):
        Partner = http.request.env['res.partner']
        partner = Partner.search([('id', '=', post.get('id'))])
        partner.unlink()
        return "Partner deleted successfully! ID: {}".format(partner.id)

