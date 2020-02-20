from django.contrib import admin
from .models import emergencycall, agency
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

# Register your models here.

class CallResource(resources.ModelResource):
    agency_id = fields.Field(
        column_name='agency',
        attribute='agency',
        widget=ForeignKeyWidget(agency, 'id'))
    
    class Meta:
        model = emergencycall

class CallAdmin(ImportExportModelAdmin):

   resource_class = CallResource
   list_display = ['id', 'description', 'place', 'received']
   verbose_name = "Incidents"

class agencyAdmin(admin.ModelAdmin):
    fields = ['name']
    verbose_name_plural = "Agencies"

admin.site.register(emergencycall, CallAdmin)
admin.site.register(agency, agencyAdmin)
admin.site.site_header = "911maps administration ";
admin.site.site_title = "911maps administration ";
