from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.ExperimentList)
# admin.site.register(models.User)
admin.site.register(models.SampleType)
admin.site.register(models.ProjectType)
admin.site.register(models.CostType)

admin.site.register(models.ResPerson)
admin.site.register(models.SupinformationExp)
admin.site.register(models.Machine)
admin.site.register(models.AdditionalCost)
admin.site.register(models.ProManager)
admin.site.register(models.PayType)
admin.site.register(models.InvoicePayment)

admin.site.register(models.UnitInvoice)
admin.site.register(models.RequireInvoice)
admin.site.register(models.ReimburseMaterial)
admin.site.register(models.TypeApply)
admin.site.register(models.ApplyInvoice)
admin.site.register(models.FilesRelated)


