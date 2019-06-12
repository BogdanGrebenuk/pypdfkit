import collections

from itertools import islice, groupby
from typing import Iterable, List

from . import abc_pdf
from . import entities
from . import helper
from . import templatemanager


__all__ = [
    "Empty",
    "PyObjToHtmlConverter"
]


def range_subset(range1, range2):
    """Whether range1 is a subset of range2."""
    if not range1:
        return True  # empty range is subset of anything
    if not range2:
        return False  # non-empty range can't be subset of empty range
    if len(range1) > 1 and range1.step % range2.step:
        return False  # must have a single value or integer multiple step
    return range1.start in range2 and range1[-1] in range2


def get_value_and_quantity(data):
    """Callback for itertools.groupby. 
    
    Returns value and number of repetitions (fetched from groupby) 
    
    """
    return data[0], len(list(data[1]))


def _add_column(ranges, range_, column, value, quantity, empty):
    """Function updates information about columns"""
    ranges.append(range_)
    column.extend(
        [entities.CellInfo(value, quantity)]
        + [entities.CellInfo(empty, None) for _ in range(quantity-1)]
    )


def group(data, level=None, *, empty):
    """Function returns grouped data"""
    if not data or not data[0]: # если данных нет, возвращаем их
        return data
    # установка кол-ва столбцов для группировки
    level = len(data[0])-1 if level is None else level
    # храним группированные значения предыдущей колонки для текущей 
    prev_ranges = [] 
    new_data = [] # результат работы функции будет здесь
    data = zip(*data) # транспонируем, чтобы идти по столбцам
    for column in islice(data, level):
        index = 0 # индекс указывает на позицию в столбце
        acc_column = [] # храним группированные значения 
        curr_ranges = [] # храним индексы группировки 
        for v, n in map(get_value_and_quantity, groupby(column)):
            curr_range = range(index, index + n)
            if (
                    not prev_ranges
                    or
                    any(range_subset(curr_range, r) for r in prev_ranges)
                    ): # если можно поместить полностью
                _add_column(
                    curr_ranges, curr_range, 
                    acc_column, v, n, 
                    empty
                    )
            else: # разбить на подходящие части
                new_index = index
                last_index = index + n
                # идем по отрезкам предыдущего столбца и разбиваем текущий
                for r in prev_ranges:
                    if new_index not in r:
                        continue
                    curr_range = range(new_index, last_index)
                    if range_subset(curr_range, r):
                        temp_value = last_index - new_index
                        _add_column(
                            curr_ranges, curr_range, 
                            acc_column, v, temp_value, 
                            empty
                            )
                        break
                    else:
                        new_range = range(new_index, r.stop)
                        temp_value = r.stop - new_index
                        _add_column(
                            curr_ranges, new_range, 
                            acc_column, v, temp_value, 
                            empty
                            )
                        new_index = r.stop
            index += n
        new_data.append(acc_column)
        prev_ranges = curr_ranges[:]
    for column in data: # доисчерпываем итератор
        new_data.append([entities.CellInfo(v, 1) for v in column])
    return list(zip(*new_data))


def to_html(data: List[List[entities.CellInfo]], *, empty):
    """Convert data to html table"""
    acc_table = []
    for row in data:
        acc_row = ["<tr>"]
        for elem in row:
            if elem.value == empty:
                continue
            acc_row.append(
                "<td rowspan='{}'>{}</td>".format(
                    elem.quantity, elem.value
                )
            )
        acc_row.append("</tr>")
        acc_table.append("\n".join(acc_row))
    return "\n".join(acc_table)


class Empty:
    """Class describes 'empty' cell in table"""


class PyObjToHtmlConverter(abc_pdf.AbstractPyObjToHtmlConverter):
    """Convert data from object to str (html-markup)"""

    def __init__(self, template_manager=None):
        template_manager = (
            template_manager or templatemanager.DefaultTemplateManager()
        )
        helper.check_isinstance(
            (template_manager, abc_pdf.AbstractTemplateManager)
        )
        self.template_manager = template_manager

    def convert(self, report: entities.Report) -> str:
        title = self.convert_title(
            report.title, len(report.fields)
        )
        fields = self.convert_fields(
            report.fields
        )
        html_table_data = self.convert_data(
            report.data, report.grouping
        )
        totals = self.convert_totals(
            report.totals, len(report.fields)
        )
        html_table = (
            "<table>"
            + title + fields + html_table_data + totals
            + "</table>"    
        )
        return self.template_manager.render(table=html_table)

    def convert_data(self, data, level=None, empty=Empty()):
        grouped_data = group(data, level, empty=empty)
        html_data = to_html(grouped_data, empty=empty)
        return html_data

    def convert_title(self, title, number_of_fields):
        return (
            "<tr>" 
            + "<th colspan='{}' align='center'> {} </th>".format(
                number_of_fields, title
                )
            + "</tr>"
        )   

    def convert_fields(self, fields):
        return (
            "<tr>" 
            + "".join("<th>{}</th>".format(i) for i in fields) 
            + "</tr>"
        )

    def convert_totals(
            self, 
            totals_results: List[entities.TotalsResult], 
            number_of_fields
        ):
        totals_positions = {
            t.totals_info.position: t
            for t in totals_results
        }
        totals_value = "<tr>"
        totals_title = "<tr>"
        cell_template = "<td>{}</td>"
        for position in range(number_of_fields):
            t_res = totals_positions.get(position)
            if t_res is None:
                template_title_data = ""
                template_value_data = ""
            else:
                template_title_data = t_res.totals_info.title
                template_value_data = t_res.result
            
            totals_title = (
                cell_template.format(template_title_data) 
                + totals_title
            )

            totals_value = (
                cell_template.format(template_value_data) 
                + totals_value
            )
            
        totals_value += "</td>"
        totals_title += "</td>"
        empty_line = (
            "<tr>" 
            + "<td colspan='{}'></td>".format(number_of_fields)
            + "</tr>"
        )
        return empty_line + totals_title + totals_value