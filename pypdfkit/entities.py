import collections
from typing import Any, Callable, List, Tuple


__all__ = [
    "TotalsInfo",
    "TotalsResult",
    "CellInfo",
    "Report"
]


# without dataclasses :(
class TotalsInfo:
    
    def __init__(
            self, 
            title: str,
            function: Callable,
            position: int
            ):
        """Entity describes totals field
        
        positional params:
        - title (str) - name of totals cell
        - function (Callable) - function object, processing data
        - position (int) - cell number where data will be stored 

        position starts with 0 and 0 is rightmost cell (in last row)
        
        """
        self.title = title
        self.function = function
        self.position = position


class TotalsResult:

    def __init__(
            self,
            totals_info: TotalsInfo,
            result: Any
            ):
        """Entity describes result of totals field
    
        positional params:
        - totals_info (TotalsInfo) - TotalsInfo object
        - result (Any) - result of totals_info.function function
    
        """
        self.totals_info = totals_info
        self.result = result


class CellInfo:

    def __init__(
            self, 
            value: Any,
            quantity: int
            ):
        """Entity describes cell in a column with information
        about number of 'same' underlying cells.
        
        positional params:
        - value (Any) - cell value
        - quantity (int) - number of underlying cells with same value 

        """
        self.value = value
        self.quantity = quantity


class Report:
    
    def __init__(
            self,
            title: str,
            fields: List[str],
            data: List[Tuple],
            totals: List[TotalsResult],
            grouping: List[int],
            file_name: str
            ):
        """Entity describes report.
    
        positional params:
        - title (str) - report title (topmost line of document)
        - fields (List[str]) - list of field names
        - data (List[Tuple]) - tabular data
        - totals (List[TotalsResult]) - list of TotalsResult
        - grouping (List[int]) - columns that must be grouped. If None 
        is given, data of all columns will be grouped, except the last.
        - file_name (str) - name of created file

        """
        self.title = title
        self.fields = fields
        self.data = data
        self.totals = totals
        self.grouping = grouping
        self.file_name = file_name