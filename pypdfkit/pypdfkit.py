import collections

import pdfkit

from . import abc_pdf
from . import entities
from . import helper
from . import pyobj2html


__all__ = [
    "ReportBuilder",
    "HtmlToPdfReportManager"
]


default_options = {  # https://wkhtmltopdf.org/usage/wkhtmltopdf.txt
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'footer-center': '[page]',
    'cookie': [
        ('cookie-name1', 'cookie-value1'),
        ('cookie-name2', 'cookie-value2'),
    ],
    'no-outline': None
}


class ReportBuilder:
    """Provide API for creating reports"""
    def __init__(
            self, 
            data_manager, 
            report_manager=None
            ):
        report_manager = (
            report_manager or HtmlToPdfReportManager()
        )  
        helper.check_isinstance(
            (report_manager, abc_pdf.AbstractReportManager),
            (data_manager, abc_pdf.AbstractDataManager)
        )
        self.data_manager = data_manager
        self.report_manager = report_manager

    def create_report(self, title, file_name, grouping=None):
        data = self.data_manager.get_data() 
        totals = self.data_manager.process_totals(data)
        fields = self.data_manager.get_fields()
        report_info = entities.Report(
            title, 
            fields, 
            data, 
            totals,  
            grouping, 
            file_name
        )
        return self.report_manager.create(report_info)


class HtmlToPdfReportManager(abc_pdf.AbstractReportManager):
    """Class provides API for creating PDF-files"""

    options = default_options

    def __init__(self, pyobj_to_html_converter=None, options=None):
        self.options = options or self.options
        pyobj_to_html_converter = (
            pyobj_to_html_converter or pyobj2html.PyObjToHtmlConverter()
        )
        helper.check_isinstance(
            (
                pyobj_to_html_converter, 
                abc_pdf.AbstractPyObjToHtmlConverter
            )
        )
        self.pyobj_to_html_converter = pyobj_to_html_converter

    def create(self, report_info: entities.Report):
        all_html = self.pyobj_to_html_converter.convert(report_info)
        return pdfkit.from_string(
            all_html, 
            report_info.file_name, 
            options=self.options
        )