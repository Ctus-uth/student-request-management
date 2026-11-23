from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # ==============================
    # THONG TIN SINH VIEN
    # ==============================

    student_id = fields.Char(
        string='Mã sinh viên',
        index=True
    )

    student_class = fields.Char(
        string='Lớp'
    )

    student_faculty = fields.Char(
        string='Ngành'
    )

    # ==============================
    # THONG TIN YEU CAU
    # ==============================

    request_code = fields.Char(
        string='Mã yêu cầu',
        index=True
    )

    request_type = fields.Selection(
        [
            ('confirmation', 'YC01 - Xác nhận sinh viên'),
            ('transcript', 'YC02 - Xin bảng điểm'),
            ('student_card', 'YC03 - Cấp lại thẻ sinh viên'),
            ('personal_info', 'YC04 - Điều chỉnh thông tin cá nhân'),
            ('other', 'YC05 - Đăng ký giấy tờ khác'),
            ('yc06', 'YC06 - Khiếu nại kết quả học tập'),
            ('yc07', 'YC07 - Tư vấn học vụ'),
            ('yc08', 'YC08 - Yêu cầu hỗ trợ tài khoản'),
            ('yc09', 'YC09 - Đề nghị xem xét miễn học phần'),
            ('yc10', 'YC10 - Đăng ký học lại'),
            ('yc11', 'YC11 - Đăng ký học cải thiện'),
            ('yc12', 'YC12 - Xin rút học phần'),
            ('yc13', 'YC13 - Khiếu nại hoặc phản ánh dịch vụ'),
            ('yc14', 'YC14 - Xin hoãn thi'),
            ('yc15', 'YC15 - Xin xác nhận học phí'),
            ('yc16', 'YC16 - Đề nghị hoàn trả học phí'),
            ('yc17', 'YC17 - Xin giấy giới thiệu thực tập'),
            ('yc18', 'YC18 - Xét điều kiện tốt nghiệp'),
            ('yc19', 'YC19 - Đăng ký xét học bổng'),
            ('yc20', 'YC20 - Báo lỗi cổng thông tin sinh viên'),
        ],
        string='Loại yêu cầu'
    )

    request_received_date = fields.Date(
        string='Ngày tiếp nhận',
        default=fields.Date.context_today
    )

    request_description = fields.Text(
        string='Nội dung yêu cầu'
    )

    # ==============================
    # THONG TIN XU LY
    # ==============================

    request_department = fields.Selection(
        [
            ('student_affairs', 'Phòng Công tác sinh viên'),
            ('training', 'Phòng Đào tạo'),
            ('it', 'Phòng Công nghệ thông tin'),
            ('finance', 'Phòng Tài chính – Kế toán'),
        ],
        string='Phòng hỗ trợ'
    )

    request_due_date = fields.Date(
        string='Ngày dự kiến hoàn thành'
    )

    # ==============================
    # TRANG THAI QUA HAN
    # ==============================

    request_is_overdue = fields.Boolean(
        string='Quá hạn xử lý',
        compute='_compute_request_is_overdue',
        store=True,
        index=True
    )

    @api.depends(
        'request_due_date',
        'stage_id',
        'stage_id.name'
    )
    def _compute_request_is_overdue(self):
        today = fields.Date.today()

        for record in self:
            is_completed = (
                record.stage_id
                and record.stage_id.name == '05 - Hoàn tất'
            )

            record.request_is_overdue = bool(
                record.request_due_date
                and record.request_due_date < today
                and not is_completed
            )

    request_supplement_note = fields.Text(
        string='Nội dung cần sinh viên bổ sung'
    )

    resolution = fields.Text(
        string='Kết quả xử lý'
    )

    completion_date = fields.Date(
        string='Ngày hoàn tất'
    )

    # ==============================
    # KIEM TRA MA YEU CAU
    # ==============================

    _sql_constraints = [
        (
            'request_code_unique',
            'unique(request_code)',
            'Mã yêu cầu đã tồn tại. Vui lòng sử dụng mã khác.'
        ),
    ]

    @api.constrains('request_code')
    def _check_request_code_unique(self):
        for record in self:
            code = (record.request_code or '').strip()

            if not code:
                continue

            duplicate = self.search([
                ('id', '!=', record.id),
                ('request_code', '=ilike', code),
            ], limit=1)

            if duplicate:
                raise ValidationError(
                    'Mã yêu cầu "%s" đã được sử dụng. '
                    'Vui lòng nhập mã yêu cầu khác.' % code
                )


       
    # ==============================
    # TU DONG CAP NHAT QUA HAN HANG NGAY
    # ==============================

    
    @api.model
    def _cron_update_request_overdue(self):
        """Tu dong cap nhat trang thai qua han hang ngay."""

        today = fields.Date.today()

        # Tim giai doan Hoan tat bang Odoo ORM
        completed_stage = self.env['crm.stage'].with_context(
            lang='vi_VN'
        ).search([
            ('name', '=', '05 - Hoàn tất')
        ])

        # Tim cac yeu cau da qua han va chua hoan tat
        overdue_domain = [
            ('request_due_date', '<', today)
        ]

        if completed_stage:
            overdue_domain.append(
                ('stage_id', 'not in', completed_stage.ids)
            )

        overdue_records = self.sudo().search(overdue_domain)

        if overdue_records:
            overdue_records.write({
                'request_is_overdue': True
            })

        # Reset trang thai neu khong con qua han
        # hoac yeu cau da hoan tat
        reset_domain = [
            '&',
            ('request_is_overdue', '=', True),
            '|', '|',
            ('request_due_date', '=', False),
            ('request_due_date', '>=', today),
            ('stage_id', 'in', completed_stage.ids)
        ]

        reset_records = self.sudo().search(reset_domain)

        if reset_records:
            reset_records.write({
                'request_is_overdue': False
            })



    # ==============================
    # KIEM TRA DIEU KIEN HOAN TAT
    # ==============================

    @api.constrains('stage_id', 'resolution', 'completion_date')
    def _check_request_completion(self):
        for record in self:
            if record.stage_id.name == '05 - Hoàn tất':
                if not record.resolution or not record.resolution.strip():
                    raise ValidationError(
                        'Vui lòng nhập Kết quả xử lý trước khi hoàn tất yêu cầu.'
                    )

                if not record.completion_date:
                    raise ValidationError(
                        'Yêu cầu hoàn tất phải có Ngày hoàn tất.'
                    )

    # ==============================
    # KIEM TRA YEU CAU BO SUNG
    # ==============================

    @api.constrains('stage_id', 'request_supplement_note')
    def _check_supplement_note(self):
        for record in self:
            if record.stage_id.name == '04 - Chờ sinh viên bổ sung':
                if not record.request_supplement_note or not record.request_supplement_note.strip():
                    raise ValidationError(
                        'Vui lòng nhập Nội dung cần sinh viên bổ sung '
                        'trước khi chuyển sang giai đoạn Chờ sinh viên bổ sung.'
                    )

    # ==============================
    # TU DONG XU LY KHI TAO YEU CAU
    # ==============================

    @api.model_create_multi
    def create(self, vals_list):
        completed_stage = self.env['crm.stage'].search([
            ('name', '=', '05 - Hoàn tất')
        ], limit=1)

        for vals in vals_list:
            if isinstance(vals.get('request_code'), str):
                vals['request_code'] = vals['request_code'].strip()

            if completed_stage and vals.get('stage_id') == completed_stage.id:
                if not vals.get('completion_date'):
                    vals['completion_date'] = fields.Date.context_today(self)

        return super().create(vals_list)

    # ==============================
    # TU DONG CAP NHAT KHI DOI GIAI DOAN
    # ==============================

    def write(self, vals):
        vals = dict(vals)

        if isinstance(vals.get('request_code'), str):
            vals['request_code'] = vals['request_code'].strip()

        if 'stage_id' not in vals:
            return super().write(vals)

        completed_stage = self.env['crm.stage'].search([
            ('name', '=', '05 - Hoàn tất')
        ], limit=1)

        if not completed_stage:
            return super().write(vals)

        target_stage_id = vals['stage_id']

        leaving_records = self.filtered(
            lambda r: r.stage_id.id == completed_stage.id
            and target_stage_id != completed_stage.id
        )

        entering_records = self.filtered(
            lambda r: r.stage_id.id != completed_stage.id
            and target_stage_id == completed_stage.id
        )

        other_records = self - leaving_records - entering_records

        if leaving_records:
            leaving_vals = dict(vals)
            leaving_vals['completion_date'] = False
            super(CrmLead, leaving_records).write(leaving_vals)

        if entering_records:
            entering_vals = dict(vals)
            if not entering_vals.get('completion_date'):
                entering_vals['completion_date'] = fields.Date.context_today(self)
            super(CrmLead, entering_records).write(entering_vals)

        if other_records:
            super(CrmLead, other_records).write(vals)

        return True