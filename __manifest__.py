
{
    'name': 'Student Request Management',
    'version': '20.0.1.0.0',
    'summary': 'Quản lý tiếp nhận và xử lý yêu cầu sinh viên',
    'description': """
        Bổ sung thông tin sinh viên và thông tin xử lý
        vào CRM để quản lý yêu cầu sinh viên.
    """,
    'category': 'Services',
    'depends': ['crm', 'sale_crm', 'website'],
    'data': [
        'views/crm_lead_views.xml',
        'templates/student_request_templates.xml',
        'data/ir_cron.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
