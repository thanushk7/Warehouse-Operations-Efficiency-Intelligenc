import webbrowser
from pathlib import Path

pdf = Path("powerbi_dashboard/Warehouse Operations Efficiency Intelligence.pdf").resolve()

webbrowser.open(pdf.as_uri())