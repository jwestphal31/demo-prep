#!/usr/bin/env python3
"""
Convert markdown demo prep files to PDF
"""

import sys
import markdown
from weasyprint import HTML, CSS
from pathlib import Path


def markdown_to_pdf(md_file_path, pdf_file_path=None):
    """Convert a markdown file to PDF"""

    # Read markdown file
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

    # Add CSS styling for professional look
    css_styling = """
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            color: #333;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 0;
        }
        h2 {
            color: #34495e;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 8px;
            margin-top: 30px;
        }
        h3 {
            color: #555;
            margin-top: 20px;
        }
        a {
            color: #3498db;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        code {
            background-color: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
        }
        ul, ol {
            padding-left: 30px;
        }
        li {
            margin-bottom: 8px;
        }
        strong {
            color: #2c3e50;
        }
        hr {
            border: none;
            border-top: 2px solid #e0e0e0;
            margin: 30px 0;
        }
        blockquote {
            border-left: 4px solid #3498db;
            padding-left: 20px;
            margin-left: 0;
            color: #666;
            font-style: italic;
        }
    """

    # Create full HTML document
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
        {css_styling}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # Set default PDF output path
    if pdf_file_path is None:
        pdf_file_path = Path(md_file_path).with_suffix('.pdf')

    # Generate PDF
    HTML(string=full_html).write_pdf(pdf_file_path)

    return pdf_file_path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 md_to_pdf.py <markdown_file> [output_pdf]")
        sys.exit(1)

    md_file = sys.argv[1]
    pdf_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        output_path = markdown_to_pdf(md_file, pdf_file)
        print(f"✓ PDF generated: {output_path}")
    except Exception as e:
        print(f"✗ Error generating PDF: {e}")
        sys.exit(1)
