from django import forms
from .models import ExperimentList, InvoicePayment, ApplyInvoice
# from django.contrib.admin.widgets import AdminDateWidget


class AddExp(forms.ModelForm):
    # 定义添加项目表单

    date_preperation = forms.DateField(label="制备完成", widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    date_test = forms.DateField(label="上机日期", widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    date_searchlib = forms.DateField(label="搜库日期", widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    date_senddata = forms.DateField(label="数据发送", widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    deadline_pro = forms.DateField(label="项目截止日期", widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = ExperimentList
        fields = ['experiment_num',
                  'pro_type',
                  'sam_type',
                  'cost_type',
                  'sample_num',
                  'name_terminal',
                  'unit',
                  'name',
                  'addition_cost',
                  'date_preperation',
                  'res_person',
                  'supply_info',
                  'instrument',
                  'date_test',
                  'date_searchlib',
                  'date_senddata',
                  'pro_cost',
                  'pro_manager',
                  'pay_mode',
                  'deadline_pro',
                  'file',
                  ]


class AddInvoice(forms.ModelForm):
    # 定义添加开票表单

    date_invoice = forms.DateField(label="开票日期", widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    date_post = forms.DateField(label="发票寄送日期", widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    date_callback = forms.DateField(label="合同回收日期", widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    date_payment = forms.DateField(label="回款日期", widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = InvoicePayment
        fields = ['contract_num',
                  'num_invoice',
                  'unit_invoice',
                  'date_invoice',
                  'person_apply',
                  'cost_invoice',
                  'date_post',
                  'num_express',
                  'date_callback',
                  # 'void_red',
                  'date_payment',
                  'pro_num',
                  'pay_check',
                  ]


class ApplyInvoiceForm(forms.ModelForm):
    # 定义开票申请表单
    # c_time = forms.DateField(label="申请日期", widget=forms.DateInput(attrs={'type': 'date'}),)
    # status = forms.CharField(label="状态", widget=forms.Select())

    class Meta:
        model = ApplyInvoice
        fields = ['contract_num',
                  'unit_name',
                  'new_unit',
                  'duty_paragraph',
                  'bank',
                  'account',
                  'address',
                  'phone',
                  'cost_invoice',
                  'sheet_num',
                  'require_invoice',
                  'contract_file',
                  'list_file',
                  'report_file',
                  'address_linkman',
                  'type_apply',
                  'red_invoice',
                  'note',
                  'pro_num',
                  'person_apply',
                  'status',
                  ]
