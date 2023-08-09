from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.utils.html import format_html
from django.db.models import QuerySet

import xlsxwriter
from io import BytesIO

from eimzo.models import Key

dl_icon = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16"> 
  <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
  <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
</svg>"""  # noqa: E501


@admin.action(description="Download as excel")
def download_keys_as_excel(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet[Key]) -> HttpResponse:  # noqa: E501
    output = BytesIO()
    wb = xlsxwriter.Workbook(output, options={"remove_timezone": True})
    w = wb.add_worksheet("keys")
    number_format1 = wb.add_format({'num_format': '0'})
    number_format2 = wb.add_format({'num_format': '# ##0'})
    datetime_format = wb.add_format({'num_format': 'dd/mm/yyyy hh:mm:ss'})
    titles = [
        "№", # A
        "filename", # B
        "password", # C
        "type",     # D
        "serialnumber", #E
        "stir",     # F
        "jshshir",    # G
        "organization", # H
        "full_name",   # I
        "name",     # J
        "surname",  # K
        "location", # L
        "city",     # M
        "country",  # N
        "t",        # O
        "ou",       # P
        "uid",      # Q
        "businesscategory", # R
        "validfrom_date",   # S
        "validto_date"      # T
    ]
    
    for i, j in zip(list("ABCDEFGHIJKLMNOPQRST"), range(1, 21)):
        w.write(f"{i}1", titles[j-1])
        
    for i, key in enumerate(queryset, start=2):
        w.write_number(f"A{i}", i-1)
        w.write_string(f"B{i}", key.file.name)
        w.write(f"C{i}", key.password, number_format2)
        w.write_string(f"D{i}", key.KeyType(key.type).label)
        w.write_string(f"E{i}", key.serial_number)
        w.write_number(f"F{i}", key.stir, number_format1)
        w.write_number(f"G{i}", key.jshshir, number_format1)
        w.write_string(f"H{i}", key.organization)
        w.write_string(f"I{i}", key.full_name)
        w.write(f"J{i}", key.name)
        w.write(f"K{i}", key.surname)
        w.write(f"L{i}", key.location)
        w.write(f"M{i}", key.city)
        w.write(f"N{i}", key.country)
        w.write(f"O{i}", key.employee_type)
        w.write(f"P{i}", key.ou)
        w.write_number(f"Q{i}", key.uid, number_format1)
        w.write(f"R{i}", key.business_category)
        w.write_datetime(f"S{i}", key.valid_from, datetime_format)
        w.write_datetime(f"T{i}", key.valid_to, datetime_format)
    
    w.autofit()
    wb.close()
    output.seek(0)
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

