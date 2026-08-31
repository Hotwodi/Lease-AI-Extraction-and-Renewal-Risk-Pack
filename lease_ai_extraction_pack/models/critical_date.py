from odoo import api, fields, models


class LaeCriticalDate(models.Model):
    _name = 'lae.critical.date'
    _description = 'Critical Date Tracking'
    _inherit = ['mail.thread']
    _order = 'critical_date asc'

    name = fields.Char(string='Reference', required=True, default='New', tracking=True)
    lease_id = fields.Char(string='Lease Reference')
    date_type = fields.Selection(
        [
            ('expiry', 'Expiry'),
            ('renewal_notice', 'Renewal Notice'),
            ('escalation', 'Escalation'),
            ('option_deadline', 'Option Deadline'),
            ('rent_review', 'Rent Review'),
        ],
        string='Date Type',
        required=True,
        default='expiry',
        tracking=True,
    )
    critical_date = fields.Date(string='Critical Date', required=True, tracking=True)
    days_until = fields.Integer(
        string='Days Until',
        compute='_compute_days_until',
        store=True,
    )
    alert_sent = fields.Boolean(string='Alert Sent', default=False)
    ai_priority = fields.Float(string='AI Priority', digits=(5, 2))
    state = fields.Selection(
        [
            ('upcoming', 'Upcoming'),
            ('due', 'Due'),
            ('overdue', 'Overdue'),
            ('completed', 'Completed'),
        ],
        string='Status',
        default='upcoming',
        required=True,
        tracking=True,
    )

    @api.depends('critical_date')
    def _compute_days_until(self):
        today = fields.Date.context_today(self)
        for record in self:
            if record.critical_date:
                record.days_until = (record.critical_date - today).days
            else:
                record.days_until = 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('lae.critical.date') or 'New'
        return super().create(vals_list)
