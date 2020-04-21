import xlrd
import xlwt
import os
from xlutils.copy import copy
#from models import EmpInfo, db




class ExcelMgr(object):
    filePath = ''

    def __init__(self, filePath=None):
        self.filePath = filePath

    def loadExcel(self):
        excel = xlrd.open_workbook(self.filePath)
        sheet = excel.sheet_by_index(0)
        rows = sheet.nrows
        # 清空原empInfo表
        EmpInfo.query.delete()
        db.session.commit()
        for index in range(1, rows):
            row = sheet.row_values(index)
            emp = EmpInfo(
                empID=row[0], empName=row[1], empOrg=row[2], empDep=row[3],pfRole=row[4]
            )
            db.session.add(emp)
        db.session.commit()
        return True


def saveExcel(self, datas=[], template=None, fileName=''):
    newbook = xlwt.Workbook()
    new_sheet = newbook.add_sheet('sheet1')
    start = 0
    if not None == template:
        templatePath = os.path.join(os.path.abspath('.'), 'results',template)
        workbook = xlrd.open_workbook(templatePath)
        newbook = copy(workbook)
        new_sheet = newbook.get_sheet(0)
        start = 1
    # sheets = workbook.sheet_by_index(0)
    for row in range(0, len(datas)):
        for cell in range(0, len(datas[row])):
            new_sheet.write(start + row, cell, datas[row][cell])

    save_path = os.path.join(os.path.abspath('.'), 'results', fileName)
    if os.path.exists(save_path):
        os.remove(save_path)
    newbook.save(save_path)
    return fileName
