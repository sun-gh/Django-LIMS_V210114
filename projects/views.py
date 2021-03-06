from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required

from .models import ExperimentList,  InvoicePayment, ApplyInvoice, ProjectType, UnitInvoice, FilesRelated
from .forms import AddExp, AddInvoice, ApplyInvoiceForm, UnitForm
from datetime import date, datetime
import csv
import json
from django.http import HttpResponse, JsonResponse
import os
from django.core import serializers
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
    experiment_list = ExperimentList.objects.all().order_by('-id')

    # 计算pro的剩余周期
    percent_dict = {}
    pre_dict = {}
    date_now = date.today().strftime('%Y-%m-%d')
    # 统计pro是否有开票记录
    record_inv = {}
    pros_rec = InvoicePayment.objects.values_list('pro_num', flat=True)
    pros_list = list(pros_rec)
    for i, pro in enumerate(experiment_list):
        deadline_date = pro.deadline_pro
        delta = datetime.strptime(deadline_date, '%Y-%m-%d') - datetime.strptime(date_now, '%Y-%m-%d')
        # time_percent = '{:.0%}'.format(delta.days/pro.pro_type.pro_period)
        real_period = datetime.strptime(deadline_date, '%Y-%m-%d') - datetime.strptime(pro.c_time.strftime('%Y-%m-%d'),
                                                                                       '%Y-%m-%d')
        time_percent = delta.days*100//real_period.days
        percent_dict[i] = time_percent

        # 计算前处理剩余周期
        pre_in_pro = round(pro.pro_type.pre_period / pro.pro_type.pro_period, 2)  # 前处理周期占比
        real_pre_period = int(real_period.days * pre_in_pro)   # 实际前处理周期
        passed_time = datetime.strptime(date_now, '%Y-%m-%d') - datetime.strptime(pro.c_time.strftime('%Y-%m-%d'),
                                                                                  '%Y-%m-%d')
        if real_pre_period == 0:
            pre_dict[i] = 0
        else:
            pre_percent = int((1 - passed_time.days / real_pre_period)*100)
            pre_dict[i] = pre_percent

        # 计算是否有开票
        if pro.id in pros_list:
            record_inv[i] = '有'
        else:
            record_inv[i] = '无'
    # print(percent_dict)

    return render(request, 'projects/exp_list.html', {'exp_list': experiment_list, 'per_dict': percent_dict,
                                                      'pre_dict': pre_dict, 'rec_inv': record_inv})


# 文件保存方法
def handle_uploaded_file(f):
    today = str(date.today())  # 获得今天日期
    file_name = today + '_' + f.name  # 获得上传来的文件名称,加入下划线分开日期和名称
    file_path = os.path.join(os.path.dirname(__file__), 'upload_file', file_name)  # 拼装目录名称+文件名称
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required()
def add_exp(request):

    if request.method == 'POST':
        addexp_form = AddExp(request.POST, request.FILES or None)

        if addexp_form.is_valid():

            exp_list = ExperimentList()

            exp_list.experiment_num = addexp_form.cleaned_data.get('experiment_num')
            exp_list.pro_type = addexp_form.cleaned_data.get('pro_type')
            exp_list.sam_type = addexp_form.cleaned_data.get('sam_type')
            exp_list.cost_type = addexp_form.cleaned_data.get('cost_type')
            exp_list.sample_num = addexp_form.cleaned_data.get('sample_num')
            exp_list.name_terminal = addexp_form.cleaned_data.get('name_terminal')
            exp_list.unit = addexp_form.cleaned_data.get('unit')
            exp_list.name = addexp_form.cleaned_data.get('name')
            # exp_list.addition_cost = addexp_form.cleaned_data.get('addition_cost')
            exp_list.res_person = addexp_form.cleaned_data.get('res_person')
            exp_list.second_person = addexp_form.cleaned_data.get('second_person')
            exp_list.third_person = addexp_form.cleaned_data.get('third_person')
            exp_list.fourth_person = addexp_form.cleaned_data.get('fourth_person')
            exp_list.date_pre_exp = addexp_form.cleaned_data.get('date_pre_exp')
            exp_list.date_preperation = addexp_form.cleaned_data.get('date_preperation')
            exp_list.supply_info = addexp_form.cleaned_data.get('supply_info')
            exp_list.instrument = addexp_form.cleaned_data.get('instrument')
            exp_list.date_test = addexp_form.cleaned_data.get('date_test')
            exp_list.date_searchlib = addexp_form.cleaned_data.get('date_searchlib')
            exp_list.date_senddata = addexp_form.cleaned_data.get('date_senddata')
            exp_list.pro_cost = addexp_form.cleaned_data.get('pro_cost')
            exp_list.pro_manager = addexp_form.cleaned_data.get('pro_manager')
            exp_list.pay_mode = addexp_form.cleaned_data.get('pay_mode')
            exp_list.deadline_pro = addexp_form.cleaned_data.get('deadline_pro')
            exp_list.urgent_warn = addexp_form.cleaned_data.get('urgent_warn')
            # exp_list.file = request.FILES.getlist('file')
            exp_list.save()
            # 多对多字段要单独保存
            for cost in addexp_form.cleaned_data.get('addition_cost'):
                exp_list.addition_cost.add(cost)
            # 对上传的文件单独处理
            file_list = request.FILES.getlist('file')  # 获取上传的多个文件的列表
            file_obj = []
            for file in file_list:
                file_instance = FilesRelated.objects.create(file=file)
                file_obj.append(file_instance)
            for file in file_obj:
                exp_list.files.add(file)

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
        save_pro.save()  # 此处必须添加save方法，否则数据不会保存到数据库

        # 对另外添加的文件单独处理
        file_list = request.FILES.getlist('file')  # 获取上传的多个文件的列表
        file_obj = []
        for file in file_list:
            file_instance = FilesRelated.objects.create(file=file)
            file_obj.append(file_instance)
        for file in file_obj:
            project_detail.files.add(file)

        print("项目更新成功！")
        return redirect('/projects/explist/')
    # else:
    #    pro_form = AddExp()
    #    return render(request, 'projects/pro_detail.html', locals())


@login_required()
def pro_del(request, pro_id):

    project_detail = ExperimentList.objects.get(id=pro_id)
    # sender = ExperimentList
    # file_delete(sender, project_detail, )
    project_detail.delete()
    print("项目删除成功！")
    return redirect('/projects/explist/')


@login_required()
# @permission_required('projects.can_view_invoicepayment')
def invoice_payment(request):

    invoice_list = InvoicePayment.objects.all().order_by('-id')

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

        record_red = ''
        red_rec = ApplyInvoice.objects.values_list('red_invoice', flat=True)
        red_list = list(red_rec)
        if inv_detail.id in red_list:
            record_red = '是'
        else:
            record_red = '否'

        return render(request, 'projects/inv_detail.html', {'invoice_form': invoice_form, 'inv_detail': inv_detail,
                                                            'record_red': record_red})
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

    apply_list = ApplyInvoice.objects.all().order_by('-id')

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


def unit_list(request):
    # 定义单位列表
    units = UnitInvoice.objects.all().order_by('-id')

    return render(request, 'projects/unit_list.html', {'unit_list': units})


def add_unit(request):

    if request.method == 'POST':
        unit_form = UnitForm(request.POST)
        if unit_form.is_valid():
            print("单位添加表单验证通过！")

            # 将数据添加到数据库
            unit_form.save()

            return redirect('/projects/unit_list/')
        else:
            # print("发票申请表单验证有误！")
            unit_form = UnitForm()
            return render(request, 'projects/add_unit.html', locals())
    else:
        unit_form = UnitForm()
        return render(request, 'projects/add_unit.html', locals())


def unit_detail(request, unit_id):
    # 定义客户单位的详情页

    unit = UnitInvoice.objects.get(id=unit_id)
    if request.method == 'GET':

        unit_form = UnitForm(instance=unit)

        return render(request, 'projects/unit_detail.html', {'unit_form': unit_form, 'unit_obj': unit})
    elif request.method == 'POST':
        save_unit = UnitForm(request.POST, instance=unit)  # 将更新的数据保存到数据库
        save_unit.save()  # 此处必须添加save方法，否则数据不会保存到数据库
        print("单位更新成功！")

        return redirect('/projects/unit_list/')


def unit_del(request, unit_id):

    unit = UnitInvoice.objects.get(id=unit_id)
    unit.delete()
    print("单位删除成功！")

    return redirect('/projects/unit_list/')


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


def get(request):
    # 定义ajax测试部分

    # ret = {"status": "true", "messages": None, }
    if request.method == "POST":
        print("POST请求成功!")

        if request.POST.get("type") == "post":
            # ret["messages"] = "post()方法将返回值载入标签内！"
            pro = ExperimentList.objects.get(id=request.POST.get("pro_id"))
            file = FilesRelated.objects.get(id=request.POST.get("file_id"))
            pro.files.remove(file)
            pro_form = AddExp(instance=pro)
            file_list = FilesRelated.objects.filter(experimentlist__id=request.POST.get("pro_id"))
            json_file = serializers.serialize("json", file_list)
            # print(json_file)

            return HttpResponse(json_file)

    # if request.method == "GET":
    #    print(request.GET)
    #    ret["messages"] = "get()方法返回服务器信息！"
    return HttpResponse("Not POST request")


def ajax_main(request):
    # 定义ajax测试页
    if request.method == 'POST':
        print("ajax请求到达！")
        l1 = request.POST.get('l1')
        l2 = request.POST.get('l2')
        res = int(l1) + int(l2)
        return HttpResponse(res)
    return render(request, 'projects/test.html')