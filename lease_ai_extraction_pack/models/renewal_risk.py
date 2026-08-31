from odoo import api, fields, models


class LaeRenewalRisk(models.Model):
    _name = 'lae.renewal.risk'
    _description = 'Renewal Risk Assessment'
    _inherit = ['mail.thread']
    _order = 'expiry_date desc'

    name = fields.Char(string='Reference', required=True, default='New', tracking=True)
    lease_id = fields.Char(string='Lease Reference')
    tenant_id = fields.Char(string='Tenant Reference')
    expiry_date = fields.Date(string='Expiry Date', tracking=True)
    days_until_expiry = fields.Integer(
        string='Days Until Expiry',
        compute='_compute_days_until_expiry',
        store=True,
    )
    ai_renewal_probability = fields.Float(string='AI Renewal Probability (%)', digits=(5, 2), tracking=True)
    risk_factors = fields.Text(string='Risk Factors')
    market_rent_comparison = fields.Text(string='Market Rent Comparison')
    tenant_payment_history_score = fields.Float(string='Payment History Score', digits=(5, 2))
    ai_recommendation = fields.Selection(
        [
            ('renew_proactively', 'Renew Proactively'),
            ('renegotiate_terms', 'Renegotiate Terms'),
            ('prepare_for_turnover', 'Prepare for Turnover'),
            ('monitor', 'Monitor'),
        ],
        string='AI Recommendation',
        default='monitor',
        tracking=True,
    )
    risk_level = fields.Selection(
        [
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        string='Risk Level',
        default='low',
        required=True,
        tracking=True,
    )

    @api.depends('expiry_date')
    def _compute_days_until_expiry(self):
        today = fields.Date.context_today(self)
        for record in self:
            if record.expiry_date:
                record.days_until_expiry = (record.expiry_date - today).days
            else:
                record.days_until_expiry = 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('lae.renewal.risk') or 'New'
        return super().create(vals_list)
