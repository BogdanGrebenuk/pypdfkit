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
    """Entity describes totals field
    
    __init__ positional params:
    - title (str) - name of totals cell
    - function (Callable) - function object, processing data
    - position (int) - cell number where data will be stored 

    position starts with 0 and 0 is rightmost cell (in last row)
    
    """
    def __init__(
            self, 
            title: str,
            function: Callable,
            position: int
            ):
        self.title = title
        self.function = function
        self.position = position


class TotalsResult:
    """Entity describes result of totals field
    
    __init__ positional params:
    - totals_info (TotalsInfo) - TotalsInfo object
    - result (Any) - result of totals_info.function function
    
    """

    def __init__(
            self,
            totals_info: TotalsInfo,
            result: Any
            ):
        self.totals_info = totals_info
        self.result = result


class CellInfo:
    """Entity describes cell in a column with information
    about number of 'same' underlying cells.
    
    __init__ positional params:
    - value (Any) - cell value
    - quantity (int) - number of underlying cells with same value 

    """

    def __init__(
            self, 
            value: Any,
            quantity: int
            ):
        self.value = value
        self.quantity = quantity


class Report:
    """Entity describes report.
    
    __init__ positional params:
    - title (str) - report title (topmost line of document)
    - fields (List[str]) - list of field names
    - data (List[Tuple]) - tabular data
    - totals (List[TotalsResult]) - list of TotalsResult
    - grouping (int) - number of columns that must be grouped. If None 
      is given, data of all columns will be grouped, except the last.
    - file_name (str) - name of created file

    """
    def __init__(
            self,
            title: str,
            fields: List[str],
            data: List[Tuple],
            totals: List[TotalsResult],
            grouping: int,
            file_name: str
            ):
        self.title = title
        self.fields = fields
        self.data = data
        self.totals = totals
        self.grouping = grouping
        self.file_name = file_name