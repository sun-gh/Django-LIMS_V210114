from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required

from .models import ExperimentList,  InvoicePayment, file_delete, ApplyInvoice, ProjectType, UnitInvoice
from .forms import AddExp, AddInvoice, ApplyInvoiceForm
from datetime import date, datetime
import csv
import codecs
import json
from django.http import HttpResponse
import os
from django.core.paginator import Paginator

# Create your views here.


@login_required()
def index(request):

    # 定义主页

    return render(request, "projects/index.html")


@login_required()
def explist(request):

    """ q = request.GET.get("q")
    if q:
        experiment_list = ExperimentList.objects.filter(name=q).all()
        return render(request, 'projects/exp_list.html', {'exp_list': experiment_list})
    else:"""
    experiment_list = ExperimentList.objects.all().order_by('id')

    # 计算pro的剩余周期
    percent_dict = {}
    date_now = date.today().strftime('%Y-%m-%d')
    # 统计pro是否有开票记录
    record_inv = {}
    pros_rec = InvoicePayment.objects.values_list('pro_num', flat=True)
    pros_list = list(pros_rec)
    for i, pro in enumerate(experiment_list):
        deadline_date = pro.deadline_pro
        delta = datetime.strptime(deadline_date, '%Y-%m-%d') - datetime.strptime(date_now, '%Y-%m-%d')
        time_percent = '{:.0%}'.format(delta.days/pro.pro_type.pro_period)
        percent_dict[i] = time_percent
        if pro.id in pros_list:
            record_inv[i] = '有'
        else:
            record_inv[i] = '无'
    # print(record_inv)

    return render(request, 'projects/exp_list.html', {'exp_list': experiment_list, 'per_dict': percent_dict,
                                                      'rec_inv': record_inv})


@login_required()
def add_exp(request):

    if request.method == 'POST':
        addexp_form = AddExp(request.POST, request.FILES or None)
        if addexp_form.is_valid():

            exp_list = ExperimentList()
            # ExperimentList.objects.create(
            exp_list.experiment_num = addexp_form.cleaned_data.get('experiment_num')
            exp_list.pro_type = addexp_form.cleaned_data.get('pro_type')
            exp_list.sam_type = addexp_form.cleaned_data.get('sam_type')
            exp_list.cost_type = addexp_form.cleaned_data.get('cost_type')
            exp_list.sample_num = addexp_form.cleaned_data.get('sample_num')
            exp_list.name_terminal = addexp_form.cleaned_data.get('name_terminal')
            exp_list.unit = addexp_form.cleaned_data.get('unit')
            exp_list.name = addexp_form.cleaned_data.get('name')
            # exp_list.addition_cost = addexp_form.cleaned_data.get('addition_cost')
            exp_list.date_preperation = addexp_form.cleaned_data.get('date_preperation')
            exp_list.res_person = addexp_form.cleaned_data.get('res_person')
            exp_list.supply_info = addexp_form.cleaned_data.get('supply_info')
            exp_list.instrument = addexp_form.cleaned_data.get('instrument')
            exp_list.date_test = addexp_form.cleaned_data.get('date_test')
            exp_list.date_searchlib = addexp_form.cleaned_data.get('date_searchlib')
            exp_list.date_senddata = addexp_form.cleaned_data.get('date_senddata')
            exp_list.pro_cost = addexp_form.cleaned_data.get('pro_cost')
            exp_list.pro_manager = addexp_form.cleaned_data.get('pro_manager')
            exp_list.pay_mode = addexp_form.cleaned_data.get('pay_mode')
            exp_list.deadline_pro = addexp_form.cleaned_data.get('deadline_pro')
            exp_list.file = request.FILES.get('file')
            exp_list.save()
            # 多对多字段要单独保存
            for cost in addexp_form.cleaned_data.get('addition_cost'):
                exp_list.addition_cost.add(cost)

            return redirect('/projects/explist/')
        else:
            addexp_form = AddExp()
            return render(request, 'projects/add_exp.html', locals())
    else:
        date_now = date.today()
        pro_now = ExperimentList.objects.filter(c_time__contains=date_now).order_by('-c_time')

        # 将pro_type的周期数据取出
        pro_types = ProjectType.objects.all()
        pro_dict = {}
        for pro_type in pro_types:
            pro_dict[pro_type.id] = pro_type.pro_period
        # print(pro_dict)

        if pro_now:
            experiment_num = int(pro_now[0].experiment_num) + 1
            addexp_form = AddExp({'experiment_num': experiment_num})
            return render(request, 'projects/add_exp.html', {'addexp_form': addexp_form,
                                                             'pro_dict': json.dumps(pro_dict)})
        else:
            experiment_num = date_now.strftime('%y%m%d') + '01'
            addexp_form = AddExp({'experiment_num': experiment_num})
            return render(request, 'projects/add_exp.html', {'addexp_form': addexp_form,
                                                             'pro_dict': json.dumps(pro_dict)})


@login_required()
def pro_detail(request, pro_id):

    project_detail = ExperimentList.objects.get(id=pro_id)  # 此处pro_id不能加引号''
    if request.method == 'GET':

        pro_form = AddExp(instance=project_detail)  # 通过instance获取数据库数据返回给表单

        return render(request, 'projects/pro_detail.html', {'pro_form': pro_form, 'project_detail': project_detail})
    elif request.method == 'POST':
        save_pro = AddExp(request.POST, request.FILES, instance=project_detail)   # 将更新的数据保存到数据库
        save_pro.save()   # 此处必须添加save方法，否则数据不会保存到数据库
        print("更新成功！")
        return redirect('/projects/explist/')


@login_required()
def pro_del(request, pro_id):

    project_detail = ExperimentList.objects.get(id=pro_id)
    sender = ExperimentList
    file_delete(sender, project_detail, )
    project_detail.delete()
    print("删除成功！")
    return redirect('/projects/explist/')


@login_required()
# @permission_required('projects.can_view_invoicepayment')
def invoice_payment(request):

    invoice_list = InvoicePayment.objects.all().order_by('id')

    record_red = {}
    red_rec = ApplyInvoice.objects.values_list('red_invoice', flat=True)
    red_list = list(red_rec)
    for i, inv in enumerate(invoice_list):

        if inv.id in red_list:
            record_red[i] = '是'
        else:
            record_red[i] = '否'

    '''paginator = Paginator(invoices, 3)
    page = request.GET.get('page')
    invoice_list = paginator.get_page(page)'''
    return render(request, 'projects/invoice_list.html', {'invoice_list': invoice_list, 'record_red': record_red})


@login_required()
def invoice_detail(request, inv_id):
    # 定义发票详情和修改功能

    inv_detail = InvoicePayment.objects.get(id=inv_id)  # 此处inv_id不能加引号''
    if request.method == 'GET':

        invoice_form = AddInvoice(instance=inv_detail)

        return render(request, 'projects/inv_detail.html', {'invoice_form': invoice_form, 'inv_detail': inv_detail})
    elif request.method == 'POST':
        save_inv = AddInvoice(request.POST, instance=inv_detail)  # 将更新的数据保存到数据库
        save_inv.save()  # 此处必须添加save方法，否则数据不会保存到数据库
        print("更新成功！")
        return redirect('/projects/invoice_payment/')


@login_required()
def inv_del(request, inv_id):

    inv_detail = InvoicePayment.objects.get(id=inv_id)
    inv_detail.delete()
    print("删除成功！")
    return redirect('/projects/invoice_payment/')


def applylist(request):

    apply_list = ApplyInvoice.objects.all().order_by('-c_time')

    '''paginator = Paginator(applys, 3)
    page = request.GET.get('page')
    apply_list = paginator.get_page(page)'''
    return render(request, 'projects/apply_list.html', {'apply_list': apply_list})


def applyinvoice(request):

    if request.method == 'POST':
        addapply_form = ApplyInvoiceForm(request.POST, request.FILES or None)
        if addapply_form.is_valid():
            # 此处缺少发票张数为0的判断
            print("发票申请表单验证通过！")
            apply_list = ApplyInvoice()
            # 将数据添加到数据库
            apply_list.contract_num = addapply_form.cleaned_data.get('contract_num')
            apply_list.unit_name = addapply_form.cleaned_data.get('unit_name')
            apply_list.new_unit = addapply_form.cleaned_data.get('new_unit')
            apply_list.duty_paragraph = addapply_form.cleaned_data.get('duty_paragraph')
            apply_list.bank = addapply_form.cleaned_data.get('bank')
            apply_list.account = addapply_form.cleaned_data.get('account')
            apply_list.address = addapply_form.cleaned_data.get('address')
            apply_list.phone = addapply_form.cleaned_data.get('phone')
            apply_list.cost_invoice = addapply_form.cleaned_data.get('cost_invoice')
            apply_list.sheet_num = addapply_form.cleaned_data.get('sheet_num')
            apply_list.address_linkman = addapply_form.cleaned_data.get('address_linkman')
            apply_list.type_apply = addapply_form.cleaned_data.get('type_apply')
            # apply_list.red_invoice = addapply_form.cleaned_data.get('red_invoice')
            apply_list.note = addapply_form.cleaned_data.get('note')
            apply_list.person_apply = addapply_form.cleaned_data.get('person_apply')
            # apply_list.person_apply = request.POST.get('username')
            apply_list.status = addapply_form.cleaned_data.get('status')
            apply_list.contract_file = request.FILES.get('contract_file')
            apply_list.list_file = request.FILES.get('list_file')
            apply_list.report_file = request.FILES.get('report_file')

            apply_list.save()  # 此处只能将多对多字段单独保存
            for require in addapply_form.cleaned_data.get('require_invoice'):
                apply_list.require_invoice.add(require)
            # for material in addapply_form.cleaned_data.get('reimburse_material'):
            #    apply_list.reimburse_material.add(material)
            for invoice in addapply_form.cleaned_data.get('red_invoice'):
                apply_list.red_invoice.add(invoice)
            for pro in addapply_form.cleaned_data.get('pro_num'):
                apply_list.pro_num.add(pro)

            return redirect('/projects/applylist/')
        else:
            print("发票申请表单验证有误！")
            applyinvoice_form = ApplyInvoiceForm()
            return render(request, 'projects/apply_invoice.html', locals())
    else:
        applyinv_form = ApplyInvoiceForm()
        return render(request, 'projects/apply_invoice.html', locals())


def apply_detail(request, apply_id):

    #  定义开票申请详情页

    aly_detail = ApplyInvoice.objects.get(id=apply_id)  # 此处apply_id不能加引号''
    if request.method == 'GET':

        apply_form = ApplyInvoiceForm(instance=aly_detail)

        return render(request, 'projects/apply_detail.html', {'apply_form': apply_form, 'aly_detail': aly_detail})
    elif request.method == 'POST':
        save_aly = ApplyInvoiceForm(request.POST, request.FILES, instance=aly_detail)  # 将更新的数据保存到数据库
        save_aly.save()  # 此处必须添加save方法，否则数据不会保存到数据库
        print("开票记录更新成功！")

        return redirect('/projects/applylist/')


def approve_apply(request, apply_id):

    #  定义审批开票申请

    aly_detail = ApplyInvoice.objects.get(id=apply_id)  # 此处apply_id不能加引号''
    aly_detail.status = "PD"
    aly_detail.save()

    start_num = 1
    date_now = date.today().strftime('%Y-%m-%d')
    while start_num <= aly_detail.sheet_num:

        invpay = InvoicePayment()
        invpay.contract_num = aly_detail.contract_num
        if aly_detail.unit_name is not None:
            invpay.unit_invoice = aly_detail.unit_name
        else:
            invpay.unit_invoice = aly_detail.new_unit
        invpay.date_invoice = date_now   # 将审批时间作为开票时间
        invpay.person_apply = aly_detail.person_apply
        invpay.save()
        for pro in aly_detail.pro_num.all():
            invpay.pro_num.add(pro)
        print("开票成功！")
        start_num += 1
    return redirect('/projects/applylist/')


def apply_del(request, apply_id):
    apply = ApplyInvoice.objects.get(id=apply_id)
    apply.delete()
    print("删除成功！")
    return redirect('/projects/applylist/')


def test(request):
    # 暂定义单位信息导入功能
    path_ab = os.path.dirname(__file__)
    fin = open(path_ab+"/unit.txt", 'rt', encoding='UTF-8')
    lines = fin.readlines()  # 返回字符串列表
    fin.close()
    for line in lines:
        unit = UnitInvoice(unit_name=line)
        unit.save()

    return render(request, 'projects/test.html')