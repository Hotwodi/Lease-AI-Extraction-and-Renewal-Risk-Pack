from odoo import fields, models


class LaeLeaseField(models.Model):
    _name = 'lae.lease.field'
    _description = 'Extracted Lease Field'
    _order = 'job_id, field_category, id'

    name = fields.Char(string='Reference', required=True, default='New')
    job_id = fields.Many2one('lae.extraction.job', string='Extraction Job', required=True, ondelete='cascade')
    field_category = fields.Selection(
        [
            ('dates', 'Dates'),
            ('rent', 'Rent'),
            ('escalation', 'Escalation'),
            ('deposits', 'Deposits'),
            ('renewal', 'Renewal'),
            ('cam', 'CAM'),
            ('clauses', 'Clauses'),
            ('parties', 'Parties'),
        ],
        string='Category',
        required=True,
        default='dates',
    )
    field_name = fields.Char(string='Field Name', required=True)
    field_value = fields.Text(string='Field Value')
    confidence = fields.Float(string='Confidence (%)', digits=(5, 2))
    page_reference = fields.Integer(string='Page Reference')
    verified = fields.Boolean(string='Verified', default=False)
    corrected_value = fields.Text(string='Corrected Value')
