from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import io

def make_pdf(summary_text: str, charts_bytes: dict) -> bytes:
    """
    charts_bytes: dict[str -> bytes] where each bytes is PNG image bytes
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20*mm, height - 20*mm, "Transaction Analyzer Report")
    c.setFont("Helvetica", 10)
    y = height - 30*mm
    for line in summary_text.splitlines():
        c.drawString(20*mm, y, line)
        y -= 6*mm
        if y < 30*mm:
            c.showPage()
            y = height - 20*mm
    # Add charts
    for title, img_bytes in charts_bytes.items():
        c.showPage()
        c.setFont("Helvetica-Bold", 12)
        c.drawString(20*mm, height - 20*mm, title)
        c.drawInlineImage(io.BytesIO(img_bytes), 20*mm, height/2 - 60*mm, width=160*mm, height=100*mm)
    c.save()
    buffer.seek(0)
    return buffer.read()
