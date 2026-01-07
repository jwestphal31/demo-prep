#!/usr/bin/env python3
"""
Demo Prep Tool - Web Interface
Run locally with: python3 web_app.py
"""

from flask import Flask, render_template, request, jsonify, send_file, session
import os
import secrets
from datetime import datetime
from demo_prep import CompanyResearcher, WebSearcher, MarkdownGenerator
from convert_to_pdf import parse_markdown_to_pdf
from pathlib import Path

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Configure upload folder
OUTPUT_FOLDER = Path('web_outputs')
OUTPUT_FOLDER.mkdir(exist_ok=True)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/research', methods=['POST'])
def research():
    """Start research process"""
    data = request.json
    domain = data.get('domain', '').strip()
    company_name = data.get('company_name', '').strip() or None
    company_context = data.get('company_context', '').strip() or None
    contact_leads = data.get('contact_leads', [])

    if not domain:
        return jsonify({'error': 'Domain is required'}), 400

    # Validate contact_leads structure
    if contact_leads and not isinstance(contact_leads, list):
        return jsonify({'error': 'contact_leads must be an array'}), 400

    # Clean and validate contacts
    validated_contacts = []
    for contact in contact_leads:
        if isinstance(contact, dict) and contact.get('name'):
            validated_contacts.append({
                'name': contact.get('name', '').strip(),
                'title': contact.get('title', '').strip(),
                'email': contact.get('email', '').strip()
            })

    # Clean domain
    domain = domain.replace('https://', '').replace('http://', '').strip('/')

    # Initialize web searcher
    web_searcher = WebSearcher()

    if not web_searcher.api_key:
        return jsonify({
            'error': 'Web search not configured. Set GOOGLE_API_KEY and GOOGLE_SEARCH_ENGINE_ID environment variables.'
        }), 400

    # Create researcher
    researcher = CompanyResearcher(
        domain,
        web_searcher=web_searcher,
        company_name_override=company_name,
        company_context=company_context,
        contact_leads=validated_contacts
    )

    # Do initial research
    researcher.research_website()
    researcher.get_company_info()

    # Prepare verification data
    verification_data = {
        'company_name': researcher.company_name,
        'domain': researcher.domain,
        'context': researcher.company_context,
        'website_info': researcher.data.get('website_info', {}),
        'company_info': researcher.data.get('company_info', {})
    }

    # Store session data for continuation
    session['research_data'] = {
        'domain': domain,
        'company_name': company_name,
        'company_context': company_context,
        'contact_leads': validated_contacts
    }

    return jsonify({
        'status': 'verification_needed',
        'data': verification_data
    })

@app.route('/api/continue', methods=['POST'])
def continue_research():
    """Continue research after verification"""
    data = request.json
    updated_context = data.get('context', '').strip() or None

    # Get session data
    research_data = session.get('research_data')
    if not research_data:
        return jsonify({'error': 'No research session found'}), 400

    domain = research_data['domain']
    company_name = research_data['company_name']
    company_context = updated_context or research_data['company_context']
    contact_leads = research_data.get('contact_leads', [])

    # Initialize web searcher
    web_searcher = WebSearcher()

    # Create researcher
    researcher = CompanyResearcher(
        domain,
        web_searcher=web_searcher,
        company_name_override=company_name,
        company_context=company_context,
        contact_leads=contact_leads
    )

    # Do full research
    researcher.research_website()
    researcher.get_company_info()
    researcher.research_tech_stack()
    researcher.research_security_vendors()
    researcher.research_security_leadership()
    researcher.research_executive_leadership()
    researcher.enrich_contact_leads()

    # Generate output files
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    company_slug = domain.split('.')[0]

    md_filename = f"{company_slug}_{timestamp}.md"
    pdf_filename = f"{company_slug}_{timestamp}.pdf"

    md_path = OUTPUT_FOLDER / md_filename
    pdf_path = OUTPUT_FOLDER / pdf_filename

    # Generate markdown
    MarkdownGenerator.generate(researcher.data, str(md_path))

    # Generate PDF
    parse_markdown_to_pdf(str(md_path), str(pdf_path))

    # Prepare results
    results = {
        'status': 'complete',
        'company_name': researcher.company_name,
        'domain': researcher.domain,
        'data': {
            'website_info': researcher.data.get('website_info', {}),
            'company_info': researcher.data.get('company_info', {}),
            'tech_stack': researcher.data.get('tech_stack', []),
            'security_vendors': researcher.data.get('security_vendors', []),
            'security_leadership': researcher.data.get('security_leadership', []),
            'executive_leadership': researcher.data.get('executive_leadership', []),
            'contact_leads': researcher.data.get('contact_leads', [])
        },
        'files': {
            'markdown': md_filename,
            'pdf': pdf_filename
        }
    }

    return jsonify(results)

@app.route('/api/download/<filename>')
def download(filename):
    """Download generated file"""
    file_path = OUTPUT_FOLDER / filename

    if not file_path.exists():
        return jsonify({'error': 'File not found'}), 404

    return send_file(
        file_path,
        as_attachment=True,
        download_name=filename
    )

@app.route('/health')
def health():
    """Health check endpoint"""
    web_searcher = WebSearcher()

    return jsonify({
        'status': 'healthy',
        'web_search_enabled': bool(web_searcher.api_key),
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("=" * 60)
    print("Demo Prep Tool - Web Interface")
    print("=" * 60)
    print()

    # Check if API keys are configured
    web_searcher = WebSearcher()
    if web_searcher.api_key:
        print("✓ Web search enabled")
    else:
        print("⚠ WARNING: Web search not configured!")
        print("  Set GOOGLE_API_KEY and GOOGLE_SEARCH_ENGINE_ID")
        print("  The web app will not work without these.")

    print()
    print("Starting server...")
    print("Open your browser to: http://localhost:5001")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()

    app.run(debug=True, host='0.0.0.0', port=5001)
