from odoo import api, fields, models


class LaeExtractionJob(models.Model):
    _name = 'lae.extraction.job'
    _description = 'Lease Extraction Job'
    _inherit = ['mail.thread']
    _order = 'created_date desc'

    name = fields.Char(string='Job Reference', required=True, default='New', tracking=True)
    document_file = fields.Binary(string='Document', attachment=True)
    document_filename = fields.Char(string='Document Filename')
    document_type = fields.Selection(
        [
            ('lease', 'Lease'),
            ('amendment', 'Amendment'),
            ('renewal_letter', 'Renewal Letter'),
            ('cam_statement', 'CAM Statement'),
        ],
        string='Document Type',
        default='lease',
        required=True,
        tracking=True,
    )
    state = fields.Selection(
        [
            ('uploaded', 'Uploaded'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
            ('reviewed', 'Reviewed'),
        ],
        string='Status',
        default='uploaded',
        required=True,
        tracking=True,
    )
    ai_confidence = fields.Float(string='AI Confidence (%)', digits=(5, 2))
    page_count = fields.Integer(string='Page Count')
    extracted_field_count = fields.Integer(
        string='Extracted Fields',
        compute='_compute_extracted_field_count',
        store=True,
    )
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user, readonly=True)
    created_date = fields.Datetime(string='Created Date', default=fields.Datetime.now, readonly=True)
    field_ids = fields.One2many('lae.lease.field', 'job_id', string='Extracted Fields')

    @api.depends('field_ids')
    def _compute_extracted_field_count(self):
        for job in self:
            job.extracted_field_count = len(job.field_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('lae.extraction.job') or 'New'
        return super().create(vals_list)
