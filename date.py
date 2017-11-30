import xlrd
from xlwt import Workbook
import datetime


def xldateToDatetime(book, sheet, row, col):
    y, m, d, h, i, s = xlrd.xldate_as_tuple(sheet.cell_value(row, col), book.datemode)
    return datetime.date(y, m, d)


def produceInit(filename="init.xls"):
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_name("init")
    init = {}

    if sheet == None:
        return None

    init["target"] = sheet.cell(0, 1).value
    xldateToDatetime(book, sheet, 1, 1)
    init["year"] = {
        "from": xldateToDatetime(book, sheet, 1, 1),
        "to": xldateToDatetime(book, sheet, 1, 2)
    }

    init["excludes"] = []
    for row in range(2, sheet.nrows):
        vals = sheet.row_values(row)
        if vals[0] == "excludes":
            init["excludes"].append(
                [
                    xldateToDatetime(book, sheet, row, 1),
                    xldateToDatetime(book, sheet, row, 2)
                ]
            )
        else:
            break

    rowStart = row + 3
    rowEnd = rowStart + 6
    un = []
    answer = {}
    for i, row in enumerate(range(rowStart, rowEnd + 1), start=1):
        init[i] = sheet.row_values(row)[2:]
        for cl in init[i]:
            if (cl not in un) and (cl != ""):
                un.append(cl)
                answer[cl] = {'date': "", 'excludes': 0, 'includes': 0, 'half': [0, 0]}

    return init, answer


def evaluateDate(init, answer):
    currentDay = init['year']['from']
    half = datetime.date(2017, 12, 31)  # TODO

    while currentDay <= init['year']['to']:

        if (not any(ex[0] <= currentDay <= ex[1] for ex in init['excludes'])):
            for cl in answer.keys():
                if cl in init[currentDay.isoweekday()] and init[currentDay.isoweekday()].count(cl) > 0:
                    answer[cl]['date'] += '{}\n'.format(currentDay.strftime('%d.%m.%Y')) * \
                        init[currentDay.isoweekday()].count(cl)
                    answer[cl]['includes'] += init[currentDay.isoweekday()].count(cl)
                    answer[cl]['half'][int(currentDay >= half)
                                       ] += init[currentDay.isoweekday()].count(cl)
        else:
            for cl in answer.keys():
                if cl in init[currentDay.isoweekday()]:
                    answer[cl]['excludes'] += init[currentDay.isoweekday()].count(cl)

        currentDay += datetime.timedelta(days=1)

    return answer


def saveAnswerToXls(answer, dest="tmp.xls"):
    book = Workbook(encoding="utf-8")

    for cl in answer.keys():
        sheet = book.add_sheet(cl, cell_overwrite_ok=True)

        sheet.col(0).width = 5000
        sheet.col(1).width = 4000

        sheet.write(0, 0, "Всего часов:")
        sheet.write(0, 1, answer[cl]['excludes'] + answer[cl]['includes'])

        sheet.write(1, 0, "Учебных часов:")
        sheet.write(1, 1, answer[cl]['includes'])

        sheet.write(2, 0, "Пропущено:")
        sheet.write(2, 1, answer[cl]['excludes'])

        sheet.write(2, 0, "По полугодиям:")
        sheet.write(2, 1, answer[cl]['half'][0])
        sheet.write(2, 2, answer[cl]['half'][1])

        for row, d in enumerate(answer[cl]['date'].split("\n"), start=4):
            sheet.write(row, 0, row - 3)
            sheet.write(row, 1, d)

    book.save(dest)


init, answer = produceInit()
answer = evaluateDate(init, answer)
saveAnswerToXls(answer, init["target"])
