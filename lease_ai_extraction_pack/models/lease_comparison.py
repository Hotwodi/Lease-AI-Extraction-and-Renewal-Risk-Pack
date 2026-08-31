from odoo import fields, models


class LaeLeaseComparison(models.Model):
    _name = 'lae.lease.comparison'
    _description = 'Lease Comparison Analysis'
    _order = 'id desc'

    name = fields.Char(string='Reference', required=True, default='New')
    lease_a_id = fields.Char(string='Lease A Reference', required=True)
    lease_b_id = fields.Char(string='Lease B Reference', required=True)
    comparison_type = fields.Selection(
        [
            ('rent', 'Rent'),
            ('terms', 'Terms'),
            ('escalation', 'Escalation'),
            ('cam', 'CAM'),
            ('deposits', 'Deposits'),
        ],
        string='Comparison Type',
        required=True,
        default='rent',
    )
    differences = fields.Text(string='Differences')
    ai_favorability = fields.Text(string='AI Favorability')
    recommendation = fields.Text(string='Recommendation')
