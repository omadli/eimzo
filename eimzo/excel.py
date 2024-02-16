import xlsxwriter
from io import BytesIO
from django.db.models import QuerySet

from eimzo.models import Key


def download_as_excel_full(queryset: QuerySet[Key]) -> BytesIO:
    output = BytesIO()
    wb = xlsxwriter.Workbook(output, options={"remove_timezone": True})
    w = wb.add_worksheet("keys")
    w.freeze_panes(1, 1)
    bold = wb.add_format({'bold': True})
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
    
    len_table = len(queryset) + 1
    w.add_table(f"A1:T{len_table}", 
        {
            "header_row": True, 
            "name": "keys",
            "columns": [{"header": i, "header_format": bold} for i in titles]
        }
    )
        
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
    return output

def download_as_excel_short(queryset: QuerySet[Key]) -> BytesIO:
    # queryset = queryset.order_by("valid_to")
    output = BytesIO()
    wb = xlsxwriter.Workbook(output, options={"remove_timezone": True})
    w = wb.add_worksheet("keys")
    w.freeze_panes(1, 1)
    bold = wb.add_format({'bold': True})
    number_format1 = wb.add_format({'num_format': '0'})
    number_format2 = wb.add_format({'num_format': '# ##0'})
    datetime_format = wb.add_format({'num_format': 'dd/mm/yyyy hh:mm:ss'})
    
    titles = [
        "№", # A
        "Fayl", # B
        "Parol", # C
        "Turi",  # D
        "SerialNumber", #E
        "STIR",     # F
        "KORXONA", # G
        "RAHBAR STIR", # H
        "RAHBAR",   # I
        "JSHSHIR",    # J
        "OLINGAN SANASI",   # K
        "YAROQLILIK MUDDATI" # L
    ]
    
    len_table = len(queryset) + 1
    w.add_table(f"A1:L{len_table}", 
        {
            "header_row": True, 
            "name": "keys",
            "columns": [{"header": i, "header_format": bold} for i in titles]
        }
    )
        
    for i, key in enumerate(queryset, start=2):
        w.write_number(f"A{i}", i-1)
        w.write_string(f"B{i}", key.file.name)
        w.write(f"C{i}", key.password, number_format2)
        w.write_string(f"D{i}", key.KeyType(key.type).label)
        w.write_string(f"E{i}", key.serial_number)
        w.write_number(f"F{i}", key.stir, number_format1)
        w.write_string(f"G{i}", key.organization.upper())
        w.write_number(f"H{i}", key.uid, number_format1)
        w.write_string(f"I{i}", key.full_name.upper())
        w.write_number(f"J{i}", key.jshshir, number_format1)
        w.write_datetime(f"K{i}", key.valid_from, datetime_format)
        w.write_datetime(f"L{i}", key.valid_to, datetime_format)
    
    w.autofit()
    wb.close()
    output.seek(0)
    return output

