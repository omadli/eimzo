from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.utils.html import format_html
from django.db.models import QuerySet

from eimzo.models import Key
from eimzo.excel import download_as_excel

dl_icon = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16"> 
  <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
  <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
</svg>"""  # noqa: E501


@admin.action(description="Download as excel")
def download_keys_as_excel(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet[Key]) -> HttpResponse:  # noqa: E501
    output = download_as_excel(queryset)
    response = HttpResponse(
        output.read(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename=certificates.xlsx'
    return response
    
    
class KeyAdmin(admin.ModelAdmin):
    list_display = ('id', 'serial_number', 'type', 'stir', 'organization_visible', "director_stir", 'full_name_visible', 'password', 'file_dl')  # noqa: E501
    list_display_links = ('id', 'serial_number',)
    list_filter = ('type', 'valid_to',)
    search_fields = ("organization", "stir", "uid", "full_name", "serial_number")
    actions = (download_keys_as_excel, )
    readonly_fields = ["serial_number", "stir", "uid", "jshshir", "city", "country", "valid_from", "valid_to"]  # noqa: E501
    
    fieldsets = [
        (
            None,
            {
                "fields": ["file", "password", "type", "serial_number", ("stir", "organization"), ("uid", "full_name", "jshshir")]  # noqa: E501
            }
        ),
        (
            "Advanced properties",
            {
                "classes": ["collapse"],
                "fields": [("name", "surname"), ("location", "city", "country"), ("employee_type", "ou", "business_category")]  # noqa: E501
            },
        ),
        (
            "Valid datetimes",
            {
                "fields": ["valid_from", "valid_to"],
            },
        ),
    ]
    
    @admin.display(ordering="organization", description="Organization")
    def organization_visible(self, obj: Key):
        return obj.organization.upper()
    
    @admin.display(ordering="full_name", description="Full name")
    def full_name_visible(self, obj: Key):
        return obj.full_name.upper()
    
    @admin.display(ordering="uid", description="Director STIR", empty_value="")
    def director_stir(self, obj: Key):
        return obj.uid
    
    @admin.display(ordering="file", description="File")
    def file_dl(self, obj: Key):
        return format_html(f"<a href='{obj.file.url}' download>{dl_icon}</a>")
        
    
admin.site.register(Key, KeyAdmin)

