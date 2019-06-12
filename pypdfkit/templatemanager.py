import jinja2

from . import abc_pdf


__all__ = [
    "DefaultTemplateManager"
]


default_template = """
<html>
<head>
    <style type="text/css">
    table {
        font-family: "Courier New", monospace;
        text-align: left;
        border-collapse: separate;
        border-spacing: 5px;
        background: #ECE9E0;
        color: #262726;
        border: 16px solid #ECE9E0;
        border-radius: 20px;
        width: 100%;
    }
    th {
        font-size: 30px;
        padding: 10px;
        text-align: center;
    }
    td {
        background: #F5D7BF;
        padding: 10px;
        font-size: 23px;
    }
    </style>
</head>
<body>
	{{table}}
</body>
</html>
"""


class DefaultTemplateManager(abc_pdf.AbstractTemplateManager):
    """Class provides rendering data from template"""

    template = default_template

    def __init__(self, template=None):
        self.template = template or self.template

    def render(self, **kwargs) -> str:
        template_loader = jinja2.BaseLoader
        template = jinja2.Environment(loader=template_loader).from_string(self.template)
        output_text = template.render(**kwargs)
        return output_text