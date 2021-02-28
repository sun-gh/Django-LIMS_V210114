from django.urls import path
from . import views

#  定义项目和开票url
app_name = 'projects'

urlpatterns = [

    path('index/', views.index, name='index'),
    # 项目管理
    path('explist/', views.explist, name='pro_list'),
    path('add_exp/', views.add_exp, name='add_exp'),
    path('pro/<int:pro_id>/', views.pro_detail),
    path('del_pro/<int:pro_id>/', views.pro_del),

    # 开票回款
    path('invoice_payment/', views.invoice_payment, name='invoice_list'),
    path('invoice/<int:inv_id>/', views.invoice_detail),
    path('del_inv/<int:inv_id>/', views.inv_del),

    # 开票申请记录
    path('applylist/', views.applylist, name='apply_list'),   # 定义开票申请列表链接
    path('apply/<int:apply_id>/', views.apply_detail, name='apply_detail'),
    path('del_apply/<int:apply_id>/', views.apply_del),
    # 审批开票申请
    path('approve_apply/<int:apply_id>/', views.approve_apply, name='approve_apply'),

    # 开票申请
    path('applyinvoice/', views.applyinvoice, name='apply_inv'),  # 定义开票申请链接

    # 导出数据
    # path('export_pro/', views.export_pro_csv),
    # path('export_inv/', views.export_inv_csv),

    # 暂定为单位自动导入链接
    path('test/', views.test,),
    # 定义手动添加单位链接
    path('unit_list/', views.unit_list, name='unit_list'),
    path('add_unit/', views.add_unit, name='add_unit'),
    path('unit/<int:unit_id>/', views.unit_detail, name='unit_detail'),
    path('del_unit/<int:unit_id>/', views.unit_del),
    # 定义ajax测试链接
    path('ajax/', views.get),
    path('ajax_main/', views.ajax_main),

]
