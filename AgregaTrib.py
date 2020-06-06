
import openpyxl
from django.conf import settings
import django
from project.settings import DATABASES, INSTALLED_APPS
settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
django.setup()
from Paralegapp.models import *

tribs = 'C:\\Users\\MASTER\\Desktop\\TRIB.xlsx'
wb_obj = openpyxl.load_workbook(tribs)
sheet_obj = wb_obj.active
for t in range(1, 230):
    trib = sheet_obj.cell(row=t, column=1).value
    tribu = Tribunal(tribunal=trib)
    tribu.save()
    print(tribu.tribunal)
