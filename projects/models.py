from django.db import models

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# Create your models here.


class SampleType(models.Model):
    #  定义样本类型model

    sampletype = models.CharField(max_length=64, verbose_name="样本类型", unique=True)

    class Meta:
        verbose_name = "样本类型表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sampletype


class ProjectType(models.Model):
    # 定义项目类型model

    projecttype = models.CharField(max_length=64, verbose_name="项目类型", unique=True)
    pro_period = models.PositiveSmallIntegerField(verbose_name="项目周期", null=True, blank=True)
    pre_period = models.PositiveSmallIntegerField(verbose_name="前处理周期", null=True, blank=True)

    class Meta:
        verbose_name = "项目类型表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.projecttype


class CostType(models.Model):
    #  定义收费等级model

    costtype = models.CharField(max_length=64, verbose_name="收费类型", unique=True)

    class Meta:
        verbose_name = "收费类型表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.costtype


class ResPerson(models.Model):
    # 定义实验负责人
    name = models.CharField(max_length=64, verbose_name="负责人", unique=True)

    class Meta:
        verbose_name = "实验负责人"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SupinformationExp(models.Model):
    # 定义实验偏差
    supply_info = models.CharField(max_length=128, verbose_name="实验偏差", unique=True)

    class Meta:
        verbose_name = "实验偏差类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.supply_info


class Machine(models.Model):
    # 定义上机仪器
    instrument = models.CharField(max_length=64, verbose_name="上机仪器", unique=True)

    class Meta:
        verbose_name = "仪器类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.instrument


class AdditionalCost(models.Model):
    # 定义附加收费类型
    addition_type = models.CharField(max_length=128, verbose_name="附加收费", unique=True)

    class Meta:
        verbose_name = "附加费用类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.addition_type


class ProManager(models.Model):
    # 定义项目经理
    pro_manager = models.CharField(max_length=128, verbose_name="项目经理", unique=True)

    class Meta:
        verbose_name = "项目经理列表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pro_manager


class PayType(models.Model):
    # 定义结算方式
    name = models.CharField(max_length=128, verbose_name="结算方式", unique=True)

    class Meta:
        verbose_name = "结算方式"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UnitInvoice(models.Model):

    # 定义开票单位
    unit_name = models.CharField(max_length=128, verbose_name="开票单位", unique=True)

    def __str__(self):
        return str(self.unit_name)

    class Meta:
        ordering = ["unit_name"]
        verbose_name = "开票单位"
        verbose_name_plural = verbose_name


# 定义上传文件的目录和名字
def user_directory_path(instance, filename):

    return '{0}/{1}'.format(instance.experiment_num, filename)


class FilesRelated(models.Model):

    # 定义项目相关文件
    file = models.FileField(verbose_name="相关文件", max_length=100, blank=True, null=True)
    c_time = models.DateTimeField(verbose_name="上传时间", auto_now_add=True)

    def __str__(self):

        return str(self.file)

    class Meta:
        verbose_name = "项目相关文件"
        verbose_name_plural = verbose_name


class ExperimentList(models.Model):
    # 定义项目列表

    experiment_num = models.CharField(max_length=64, verbose_name="项目编号", unique=True)
    pro_type = models.ForeignKey(ProjectType, verbose_name="项目类型", on_delete=models.CASCADE)  # default="蛋白鉴定")
    sam_type = models.ForeignKey(SampleType, verbose_name="样本类型", on_delete=models.CASCADE)
    cost_type = models.ForeignKey(CostType, verbose_name="收费等级", on_delete=models.CASCADE, blank=True, null=True)
    sample_num = models.PositiveSmallIntegerField(verbose_name="样本数量")
    name_terminal = models.CharField(max_length=128, verbose_name="送样终端", blank=True, null=True)
    # unit = models.CharField(max_length=128, verbose_name="送样单位")
    unit = models.ForeignKey(UnitInvoice, verbose_name="送样单位", on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=32, verbose_name="送样人")
    # addition_cost中是否为Foreignkey，还有待商榷
    addition_cost = models.ManyToManyField(AdditionalCost, verbose_name="附加收费", blank=True)  # 新修改
    date_preperation = models.CharField(max_length=32, verbose_name="制备完成", blank=True, null=True)
    res_person = models.ForeignKey(ResPerson, verbose_name="负责人", on_delete=models.CASCADE, blank=True, null=True)
    supply_info = models.ForeignKey(SupinformationExp, verbose_name="实验偏差", on_delete=models.CASCADE, blank=True,
                                    null=True)
    instrument = models.ForeignKey(Machine, verbose_name="上机仪器", on_delete=models.CASCADE, blank=True, null=True)
    date_test = models.CharField(max_length=64, verbose_name="上机日期", blank=True, null=True)
    date_searchlib = models.CharField(max_length=64, verbose_name="搜库日期", blank=True, null=True)
    date_senddata = models.CharField(max_length=64, verbose_name="数据发送", blank=True, null=True)
    pro_cost = models.PositiveSmallIntegerField(verbose_name="项目金额", blank=True, null=True)
    pro_manager = models.ForeignKey(ProManager, verbose_name="项目经理", on_delete=models.CASCADE, blank=True, null=True)
    pay_mode = models.ForeignKey(PayType, verbose_name="结算方式", on_delete=models.CASCADE, blank=True, null=True)
    deadline_pro = models.CharField(max_length=64, verbose_name="项目截止日期", blank=True, null=True)
    files = models.ManyToManyField(FilesRelated, verbose_name="相关文件", blank=True)
    c_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return str(self.experiment_num)

    class Meta:
        ordering = ["experiment_num"]
        verbose_name = "项目列表"
        verbose_name_plural = verbose_name


# @receiver(pre_delete, sender=ExperimentList)
# def file_delete(sender, instance, **kwargs):
    # 定义上传文件的删除方法
#    instance.files.delete(False)


class InvoicePayment(models.Model):
    # 定义开票回款表

    contract_num = models.CharField(max_length=128, verbose_name="合同编号")
    num_invoice = models.CharField(max_length=64, verbose_name="发票号", blank=True, null=True, unique=True)
    unit_invoice = models.CharField(max_length=128, verbose_name="开票单位", blank=True, null=True)
    date_invoice = models.CharField(max_length=64, verbose_name="开票日期", blank=True, null=True)
    person_apply = models.CharField(max_length=32, verbose_name="申请人")
    cost_invoice = models.PositiveIntegerField(verbose_name="发票金额", blank=True, null=True)
    date_post = models.CharField(max_length=64, verbose_name="发票寄送日期", blank=True, null=True)
    num_express = models.CharField(max_length=64, verbose_name="发票快递单号", blank=True, null=True)
    date_callback = models.CharField(max_length=64, verbose_name="合同回收日期", blank=True, null=True)
    # void_red = models.NullBooleanField(verbose_name="作废或冲红")
    date_payment = models.CharField(max_length=64, verbose_name="回款日期", blank=True, null=True)
    pro_num = models.ManyToManyField(ExperimentList, verbose_name="项目编号")
    pay_check = models.NullBooleanField(verbose_name="是否结清")
    c_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return str(self.num_invoice)

    class Meta:
        ordering = ["c_time"]
        verbose_name = "开票回款表"
        verbose_name_plural = verbose_name


class RequireInvoice(models.Model):

    # 定义开票要求
    require_content = models.CharField(max_length=128, verbose_name="开票要求")

    def __str__(self):
        return str(self.require_content)

    class Meta:

        verbose_name = "开票要求类型"
        verbose_name_plural = verbose_name


class ReimburseMaterial(models.Model):
    # 定义报账材料
    material_type = models.CharField(max_length=128, verbose_name="报账材料")

    def __str__(self):
        return self.material_type

    class Meta:
        verbose_name = "报账材料类型"
        verbose_name_plural = verbose_name


class TypeApply(models.Model):
    # 定义开票类型
    apply_type = models.CharField(max_length=128, verbose_name="开票类型")

    def __str__(self):

        return str(self.apply_type)

    class Meta:
        verbose_name = "开票类型表"
        verbose_name_plural = verbose_name


class ApplyInvoice(models.Model):

    # 定义开票申请记录模型
    APPLYING = 'AI'
    PASSED = 'PD'
    REFUSED = 'RD'

    status_type = (
        (APPLYING, '申请中'),
        (PASSED, '已通过'),
        (REFUSED, '已拒绝'),
    )
    contract_num = models.CharField(max_length=128, verbose_name="合同编号",)
    unit_name = models.ForeignKey(UnitInvoice, verbose_name="开票单位", on_delete=models.CASCADE, blank=True, null=True)
    new_unit = models.CharField(max_length=128, verbose_name="新单位名称", blank=True, null=True)
    duty_paragraph = models.CharField(max_length=256, verbose_name="税号", blank=True, null=True)
    bank = models.CharField(max_length=128, verbose_name="开户行", blank=True, null=True)
    account = models.CharField(max_length=128, verbose_name="银行账号", blank=True, null=True)
    address = models.CharField(max_length=256, verbose_name="单位地址", blank=True, null=True)
    phone = models.CharField(max_length=128, verbose_name="联系电话", blank=True, null=True)
    cost_invoice = models.PositiveIntegerField(verbose_name="发票金额")
    sheet_num = models.PositiveSmallIntegerField(verbose_name="开票张数")
    require_invoice = models.ManyToManyField(RequireInvoice, verbose_name="开票要求", blank=True)
    contract_file = models.FileField(verbose_name="合同文件", max_length=100, blank=True, null=True)
    list_file = models.FileField(verbose_name="项目清单", max_length=100, blank=True, null=True)
    report_file = models.FileField(verbose_name="检测报告", max_length=100, blank=True, null=True)
    # reimburse_material = models.ManyToManyField(ReimburseMaterial, verbose_name="报账材料", blank=True,)
    address_linkman = models.CharField(max_length=256, verbose_name="收件人信息", blank=True, null=True)
    type_apply = models.ForeignKey(TypeApply, verbose_name="开票类型", on_delete=models.CASCADE)
    red_invoice = models.ManyToManyField(InvoicePayment, verbose_name="原发票号", blank=True)  # 新修改
    note = models.CharField(max_length=256, verbose_name="备注", blank=True, null=True)
    pro_num = models.ManyToManyField(ExperimentList, verbose_name="项目编号")
    person_apply = models.CharField(max_length=32, verbose_name="申请人")
    status = models.CharField(max_length=32, verbose_name="状态", choices=status_type, default=APPLYING)  # default选择数据库的值
    c_time = models.DateTimeField(verbose_name="申请时间", auto_now_add=True)

    def __str__(self):

        return self.contract_num

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "开票申请总表"
        verbose_name_plural = verbose_name
