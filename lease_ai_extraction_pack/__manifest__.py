{
    'name': 'Lease AI Extraction & Renewal Risk Pack',
    'version': '18.0.1.0.0',
    'category': 'Productivity/AI',
    'summary': 'AI-powered lease document extraction, renewal risk assessment, and critical date tracking',
    'description': """
Lease AI Extraction & Renewal Risk Pack
=======================================

Extract lease data with AI, assess renewal risk, track critical dates, and compare leases side-by-side.
""",
    'author': 'SoftaiDev',
    'website': 'https://softaidev.pages.dev',
    'license': 'LGPL-3',
    'price': 499.99,
    'currency': 'USD',
    'depends': ['base', 'web', 'mail'],
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/extraction_job_views.xml',
        'views/lease_field_views.xml',
        'views/renewal_risk_views.xml',
        'views/critical_date_views.xml',
        'views/lease_comparison_views.xml',
        'views/menu.xml',
    ],
}
