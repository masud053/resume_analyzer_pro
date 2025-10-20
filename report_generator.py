from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from typing import Dict
import io, os

def generate_report(output_path: str, analysis: Dict, resume_preview: str):
    c = canvas.Canvas(output_path, pagesize=letter)
    text = c.beginText(40, 750)
    text.setFont('Helvetica-Bold', 14)
    text.textLine('Resume Analysis Report')
    text.setFont('Helvetica', 10)
    text.textLine('')
    text.textLine(f"Overall Score: {analysis.get('overall_score',0):.2f}")
    text.textLine('')
    text.textLine('Section scores:')
    for k,v in analysis.get('section_scores',{}).items():
        text.textLine(f" - {k}: {v:.3f}")
    text.textLine('')
    text.textLine('Top suggestions:')
    for s in analysis.get('suggestions',[]): 
        text.textLine(f" - {s}")
    text.textLine('')
    text.textLine('Resume preview (first 400 chars):')
    text.textLine(resume_preview[:400])
    c.drawText(text)
    c.showPage()
    c.save()
