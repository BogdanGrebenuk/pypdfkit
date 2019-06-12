"""Abstract classes declaration"""

import abc
from typing import List, Tuple

from . import entities


__all__ = [
    "AbstractDataManager",
    "AbstractReportManager",
    "AbstractPyObjToHtmlConverter",
    "AbstractTemplateManager"
    ]


class AbstractDataManager(abc.ABC):
    """Abstract class for data-manager objects
    
    Data-manager must provide data, fields, information about
    totals and realization of totals processing. 
    
    """

    @abc.abstractmethod
    def get_data(self) -> List[Tuple]:
        ...

    @abc.abstractmethod
    def get_fields(self) -> List[str]:
        ...

    @abc.abstractmethod
    def get_totals_info(self) -> List[entities.TotalsInfo]:
        ...

    @abc.abstractmethod
    def process_totals(
            self, 
            data: List[Tuple]
            ) -> List[entities.TotalsResult]:
        ...


class AbstractReportManager(abc.ABC):
    """Abstract class for report-manager object

    Report-manager must provide method for creating file.

    """

    @abc.abstractmethod
    def create(self, report: entities.Report):
        ...


class AbstractPyObjToHtmlConverter(abc.ABC): 
    """Abstract class for pyobj-tohmtl-converter objects
    
    PyObjToHtml-converter must provide method for 
    converting data from one type to another.
    
    """


    @abc.abstractmethod
    def convert(self, report: entities.Report) -> str:
        ...


class AbstractTemplateManager(abc.ABC):
    """Abstract class for template-manager objects

    Template-manager must provide rendering template.

    """

    @abc.abstractmethod
    def render(self, **kwargs) -> str:
        ...