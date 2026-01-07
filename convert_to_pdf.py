#!/usr/bin/env python3
"""
Convert markdown demo prep files to PDF using ReportLab
"""

import sys
import re
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER


def parse_markdown_to_pdf(md_file_path, pdf_file_path=None):
    """Convert markdown to PDF with basic formatting"""

    # Read markdown file
    with open(md_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Set default PDF output path
    if pdf_file_path is None:
        pdf_file_path = Path(md_file_path).with_suffix('.pdf')

    # Create PDF
    doc = SimpleDocTemplate(
        str(pdf_file_path),
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    # Define styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=HexColor('#2c3e50'),
        spaceAfter=30,
        spaceBefore=0
    )

    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=HexColor('#34495e'),
        spaceAfter=12,
        spaceBefore=20,
        borderWidth=1,
        borderColor=HexColor('#e0e0e0'),
        borderPadding=5
    )

    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=HexColor('#555555'),
        spaceAfter=10,
        spaceBefore=15
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=HexColor('#333333'),
        spaceAfter=10,
        leading=16
    )

    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=HexColor('#333333'),
        leftIndent=20,
        spaceAfter=8,
        leading=16
    )

    # Build document content
    story = []

    for line in lines:
        line = line.rstrip()

        if not line:
            story.append(Spacer(1, 0.1 * inch))
            continue

        # H1 - Title
        if line.startswith('# '):
            text = line[2:].strip()
            story.append(Paragraph(text, title_style))

        # H2 - Main sections
        elif line.startswith('## '):
            text = line[3:].strip()
            story.append(Paragraph(text, heading2_style))

        # H3 - Subsections
        elif line.startswith('### '):
            text = line[4:].strip()
            story.append(Paragraph(text, heading3_style))

        # Horizontal rule
        elif line.startswith('---'):
            story.append(Spacer(1, 0.2 * inch))

        # Bullet points
        elif line.startswith('- '):
            text = line[2:].strip()
            # Convert markdown links to reportlab format
            text = convert_markdown_links(text)
            story.append(Paragraph(f"• {text}", bullet_style))

        # Indented content (sub-bullets or continuation)
        elif line.startswith('  - '):
            text = line[4:].strip()
            text = convert_markdown_links(text)
            story.append(Paragraph(f"  ◦ {text}", bullet_style))

        # Bold text starting lines (like **Domain:**)
        elif line.startswith('**'):
            text = convert_markdown_formatting(line)
            story.append(Paragraph(text, body_style))

        # Italic/emphasis (like *No additional...*)
        elif line.startswith('*') and line.endswith('*'):
            text = f"<i>{line[1:-1]}</i>"
            story.append(Paragraph(text, body_style))

        # Regular paragraph
        else:
            text = convert_markdown_formatting(line)
            if text.strip():
                story.append(Paragraph(text, body_style))

    # Build PDF
    doc.build(story)

    return pdf_file_path


def convert_markdown_links(text):
    """Convert markdown links [text](url) to HTML links"""
    # Pattern: [text](url)
    pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
    return re.sub(pattern, r'<a href="\2" color="blue">\1</a>', text)


def convert_markdown_formatting(text):
    """Convert markdown bold and italic to HTML"""
    # Convert **bold**
    text = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', text)
    # Convert *italic*
    text = re.sub(r'\*([^\*]+)\*', r'<i>\1</i>', text)
    # Convert links
    text = convert_markdown_links(text)
    return text


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 convert_to_pdf.py <markdown_file> [output_pdf]")
        sys.exit(1)

    md_file = sys.argv[1]
    pdf_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        output_path = parse_markdown_to_pdf(md_file, pdf_file)
        print(f"✓ PDF generated: {output_path}")
        print(f"📍 Location: {Path(output_path).absolute()}")
    except Exception as e:
        print(f"✗ Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
