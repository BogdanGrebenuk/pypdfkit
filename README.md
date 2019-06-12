# PyPDFKit: Python-Pdfkit wrapper

PyPDFKit is a wrapper for [pdfkit] package to create PDF-based reports.

# Instalation

1. Install pypdfkit:
    ```sh
    $ pip install git+git://github.com/BogdanGrebenuk/pypdfkit.git
    ```
2. Install wkhtmltopdf:

    Debian/Ubuntu:
    ```sh
    $ sudo apt-get install wkhtmltopdf
    ```
    macOS:
    ```sh
    $ brew install caskroom/cask/wkhtmltopdf
    ```
    Warning! Version in debian/ubuntu repos have reduced functionality (because it compiled without the wkhtmltopdf QT patches), such as adding outlines, headers, footers, TOC etc. To use this options you should install static binary from wkhtmltopdf site or you can use this script.

    Windows and other options: check wkhtmltopdf [homepage] for binary installers (don't forget to set the windows enviroment variables).

# Usage

Define your data-manager class and implement "get_data" and "get_fields" methods.
"get_totals_info" and "process_totals" are already implemented in DefaultDataManager.

```python
import pypdfkit

class SimpleDataManager(pypdfkit.DefaultDataManager):

    def get_data(self):
        return [
            ("IPZ-16-1", "Bohdan", 20, "Python3"),
            ("IPZ-16-1", "Danil", 21, "Java/JS"),
            ("IPZ-16-1", "Ivan", 21, "JS"),
            ("IPZ-16-1", "Eugene", 22, "Ruby"),
            ("IPZ-17-2", "Bohdan", 20, "С#"),
            ("IPZ-17-2", "Vlad", 20, "Python3"),
            ("IPZ-18-1", "Eugene", 19, "С++"),
            ]

    def get_fields(self):
        return ("Group", "Name", "Age", "Lang")
```

Create an object of your data-manager class and pass it to ReportBuilder constructor.

```python
data_manager = SimpleDataManager()
report_builder = pypdfkit.ReportBuilder(data_manager)
report_builder.create_report("Hello world!", "test_file_name.pdf")
```

"create_report" method will create a file with name "test_file_name.pdf" and the title of report wii be "Hello world!".

# "Totals section" configuration

If you want to specify totals section, implement "get_totals_info" in your data-manager.

```python
class ConfigureDataManager(pypdfkit.DefaultDataManager):

    def get_totals_info(self):
        return [ 
            pypdfkit.TotalsInfo(
                "Sum", 
                lambda x: sum([i[-2] for i in x]), 
                1 # position of cell
                )
            ]
```

# Managers configuration

You can define the behavior of any manager by passing their objects to the constructor of the corresponding classes. The relationship between classes can be represented as follows:

``` ReportBuilder (has) ReportManager (has) PyObjToHtmlConverter (has) TemplateManager ```


For more information, see [abc_pdf.py].

License
----

MIT



[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [pdfkit]: <https://github.com/JazzCore/python-pdfkit>
   [homepage]: <http://wkhtmltopdf.org/>
   [abc_pdf.py]: <https://github.com/BogdanGrebenuk/pypdfkit/blob/master/pypdfkit/abc_pdf.py>
  
