
import base64
import mimetypes

from datetime import date, timedelta
from werkzeug.utils import secure_filename
from odoo import http
from odoo.http import request


class StudentRequestController(http.Controller):

    
    # TRANG CHỦ CHÍNH THỨC CỦA WEBSITE
    @http.route(
        '/',
        type='http',
        auth='public',
        website=True,
        methods=['GET'],
    )
    def student_home(self, **kwargs):
        return request.render(
            'student_request_management.student_home',
            {}
        )

    # TỰ ĐỘNG CHUYỂN VỀ TRANG CHỦ
    @http.route(
        '/student',
        type='http',
        auth='public',
        website=True,
        methods=['GET'],
    )
    def student_home_alias(self, **kwargs):
        return request.redirect('/')


    @http.route(
        '/student/request',
        type='http',
        auth='public',
        website=True,
        methods=['GET'],
    )
    def student_request_form(self, **kwargs):
        return request.render(
            'student_request_management.student_request_form',
            {}
        )

    def _calculate_due_date(self, working_days):
        """Tinh han xu ly theo ngay lam viec, khong tinh thu Bay va Chu Nhat."""
        due_date = date.today()
        days_added = 0

        while days_added < working_days:
            due_date += timedelta(days=1)

            if due_date.weekday() < 5:
                days_added += 1

        return due_date

    @http.route(
        '/student/request/submit',
        type='http',
        auth='public',
        website=True,
        methods=['POST'],
        csrf=True,
    )
    def student_request_submit(self, **post):

        student_name = (post.get('student_name') or '').strip()
        student_id = (post.get('student_id') or '').strip()
        student_class = (post.get('student_class') or '').strip()
        student_faculty = (post.get('student_faculty') or '').strip()
        email = (post.get('email') or '').strip().lower()
        phone = (post.get('phone') or '').strip()
        request_type = (post.get('request_type') or '').strip()
        description = (post.get('request_description') or '').strip()

        # Danh sach 20 loai yeu cau
        request_type_names = {
            'confirmation': 'Xac nhan sinh vien',
            'transcript': 'Xin bang diem',
            'student_card': 'Cap lai the sinh vien',
            'personal_info': 'Dieu chinh thong tin ca nhan',
            'other': 'Dang ky giay to khac',
            'yc06': 'Khieu nai ket qua hoc tap',
            'yc07': 'Tu van hoc vu',
            'yc08': 'Yeu cau ho tro tai khoan',
            'yc09': 'De nghi xem xet mien hoc phan',
            'yc10': 'Dang ky hoc lai',
            'yc11': 'Dang ky hoc cai thien',
            'yc12': 'Xin rut hoc phan',
            'yc13': 'Khieu nai hoac phan anh dich vu',
            'yc14': 'Xin hoan thi',
            'yc15': 'Xin xac nhan hoc phi',
            'yc16': 'De nghi hoan tra hoc phi',
            'yc17': 'Xin giay gioi thieu thuc tap',
            'yc18': 'Xet dieu kien tot nghiep',
            'yc19': 'Dang ky xet hoc bong',
            'yc20': 'Bao loi cong thong tin sinh vien',
        }

        # Quy tac tu dong phan phong ban va han xu ly
        request_rules = {
            'confirmation': {
                'department': 'student_affairs',
                'days': 2,
            },
            'transcript': {
                'department': 'training',
                'days': 3,
            },
            'student_card': {
                'department': 'student_affairs',
                'days': 5,
            },
            'personal_info': {
                'department': 'student_affairs',
                'days': 3,
            },
            'other': {
                'department': 'student_affairs',
                'days': 3,
            },
            'yc06': {
                'department': 'training',
                'days': 5,
            },
            'yc07': {
                'department': 'training',
                'days': 2,
            },
            'yc08': {
                'department': 'it',
                'days': 1,
            },
            'yc09': {
                'department': 'training',
                'days': 5,
            },
            'yc10': {
                'department': 'training',
                'days': 3,
            },
            'yc11': {
                'department': 'training',
                'days': 3,
            },
            'yc12': {
                'department': 'training',
                'days': 3,
            },
            'yc13': {
                'department': 'student_affairs',
                'days': 5,
            },
            'yc14': {
                'department': 'training',
                'days': 3,
            },
            'yc15': {
                'department': 'finance',
                'days': 3,
            },
            'yc16': {
                'department': 'finance',
                'days': 7,
            },
            'yc17': {
                'department': 'student_affairs',
                'days': 3,
            },
            'yc18': {
                'department': 'training',
                'days': 5,
            },
            'yc19': {
                'department': 'student_affairs',
                'days': 5,
            },
            'yc20': {
                'department': 'it',
                'days': 2,
            },
        }

        # Kiem tra du lieu dau vao
        if not all([
            student_name,
            student_id,
            student_class,
            email,
            request_type,
            description,
        ]) or request_type not in request_type_names:
            return request.redirect('/student/request?error=1')

        
        # Kiem tra file dinh kem truoc khi tao yeu cau
        uploaded_file = request.httprequest.files.get('attachment')
        file_content = None
        safe_filename = None
        file_mimetype = None

        if uploaded_file and uploaded_file.filename:
            # Gioi han dung luong 10 MB
            max_file_size = 10 * 1024 * 1024

            # Doc toi da 10 MB + 1 byte de phat hien file qua lon
            file_content = uploaded_file.stream.read(max_file_size + 1)

            if len(file_content) > max_file_size:
                return request.redirect('/student/request?error=2')

            # Bo qua file rong
            if not file_content:
                file_content = None
            else:
                # Lam sach ten file
                safe_filename = secure_filename(uploaded_file.filename)

                if not safe_filename:
                    return request.redirect('/student/request?error=2')

                # Xac dinh MIME type dua tren phan mo rong
                file_mimetype = (
                    mimetypes.guess_type(safe_filename)[0]
                    or 'application/octet-stream'
                )


        # Lay quy tac xu ly tu dong
        rule = request_rules[request_type]

        request_department = rule['department']
        request_due_date = self._calculate_due_date(rule['days'])

        # Tim hoac tao lien he sinh vien
        Partner = request.env['res.partner'].sudo().with_company(2)

        partner = Partner.search([
            ('name', '=ilike', student_name),
            ('email', '=ilike', email),
            ('company_id', 'in', [False, 2]),
        ], limit=1)

        if not partner:
            partner = Partner.create({
                'name': student_name,
                'email': email,
                'phone': phone,
                'company_id': 2,
            })
        else:
            partner.write({
                'name': student_name,
                'email': email,
                'phone': phone,
            })

        # Nhom tiep nhan
        team = request.env['crm.team'].sudo().browse(7).exists()

        if not team:
            return request.make_response(
                'Khong tim thay nhom tiep nhan yeu cau sinh vien.'
            )

        # Giai doan ban dau
        stage = request.env['crm.stage'].sudo().search([
            ('name', '=', '01 - Mới tiếp nhận'),
        ], limit=1)

        if not stage:
            return request.make_response(
                'Khong tim thay giai doan Moi tiep nhan.'
            )

        # Tao yeu cau trong CRM
        lead = request.env['crm.lead'].sudo().with_company(2).create({
            'company_id': 2,
            'name': request_type_names[request_type],
            'type': 'opportunity',
            'partner_id': partner.id,
            'contact_name': student_name,
            'email_from': email,
            'phone': phone,
            'team_id': team.id,
            'stage_id': stage.id,
            'student_id': student_id,
            'student_class': student_class,
            'student_faculty': student_faculty,
            'request_type': request_type,
            'request_description': description,
            'request_received_date': date.today(),
            'request_department': request_department,
            'request_due_date': request_due_date,
        })

        
        
        # Luu tai lieu dinh kem vao yeu cau CRM
        if file_content:
            request.env['ir.attachment'].sudo().create({
                'name': safe_filename,
                'raw': file_content,
                'res_model': 'crm.lead',
                'res_id': lead.id,
                'public': False,
            })


       

        return request.redirect('/student/request?submitted=1')
