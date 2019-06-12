from typing import Tuple, List

from . import abc_pdf
from . import entities


__all__ = [
    "DefaultDataManager"
]


class DefaultDataManager(abc_pdf.AbstractDataManager):
    """Data-manager with implemented get_totals_info and process_data"""

    def get_totals_info(self):
        """Default totals information - number of rows in right-down corner"""
        return [entities.TotalsInfo("Количество", len, 0)]

    def get_data(self):
        raise NotImplementedError

    def get_fields(self):
        raise NotImplementedError

    def process_totals(self, data) -> List[entities.TotalsResult]:
        """Default totals result processing"""
        return [
            entities.TotalsResult(t, t.function(data))
            for t in self.get_totals_info()
        ]