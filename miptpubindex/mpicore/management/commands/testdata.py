from django.core.management.base import BaseCommand
from mpicore.models import *

class Command(BaseCommand):
  '''Заполняет базу тестовыми значениями'''
  def handle(self, *args, **options):
    '''Все факультеты'''
    drec = MiptDepartment(id=1, name_ru='Факультет радиотехники и кибернетики', rank=8)
    drec.save()
    dgap = MiptDepartment(id=2, name_ru='Факультет общей и прикладной физики', rank=10)
    dgap.save()
    dasr = MiptDepartment(id=3, name_ru='Факультет аэрофизики и космических исследований', rank=5)
    dasr.save()
    dmcp = MiptDepartment(id=4, name_ru='Факультет молекулярной и химической физики', rank=6)
    dmcp.save()
    dpqe = MiptDepartment(id=5, name_ru='Факультет физической и квантовой электроники', rank=6)
    dpqe.save()
    dafe = MiptDepartment(id=6, name_ru='Факультет аэромеханики и летательной техники', rank=3)
    dafe.save()
    dcam = MiptDepartment(id=7, name_ru='Факультет управления и прикладной математики', rank=8)
    dcam.save()
    dppe = MiptDepartment(id=8, name_ru='Факультет проблем физики и энергетики', rank=6)
    dppe.save()
    diht = MiptDepartment(id=9, name_ru='Факультет инноваций и высоких технологий', rank=9)
    diht.save()
    dnbic = MiptDepartment(id=10, name_ru='Факультет нано-, био-, информационных и когнитивных технологий', rank=6)
    dnbic.save()
    dbmp = MiptDepartment(id=11, name_ru='Факультет биологической и медицинской физики', rank=7)
    dbmp.save()

    '''Некоторые тестовые кафедры'''
    cos = MiptChair(name_ru="Центр открытых систем и высоких технологий", rank = 2, department=dpqe)
    cos.save()
    ire = MiptChair(name_ru="ИРЭ РАН", rank=5, department=dpqe)
    ire.save()