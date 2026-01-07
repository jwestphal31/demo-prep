# Demo Prep Tool

An intelligent research tool that automatically gathers comprehensive information about companies for demo preparation. Uses web scraping, Google Custom Search API, and LinkedIn profile enrichment to create detailed research reports.

## ✨ Features

### 🔍 Company Research
- **Automated Web Scraping**: Extracts company information from websites
- **Google Custom Search Integration**: Searches LinkedIn, Crunchbase, and news sources
- **Company Verification**: Interactive verification step to ensure correct company before deep research

### 👥 Stakeholder Intelligence
- **Security Leadership Discovery**: Automatically finds CISO, VP Security, Directors, and Security Managers
- **Executive Leadership Mapping**: Identifies CEO, CTO, CFO, COO, CIO, and CPO
- **Contact Leads with LinkedIn Enrichment**: Add your own contacts and automatically retrieve their LinkedIn profiles

### 🔐 Security Analysis
- **Technology Stack Detection**: Identifies technologies from job postings
- **Security Vendor Connections**: Verifies usage of 62+ major security vendors (CrowdStrike, Splunk, Palo Alto, etc.)
- **Integration Discovery**: Finds vendor partnerships and security tool implementations

### 📄 Export & Reporting
- **Markdown Export**: Clean, formatted markdown documents
- **PDF Generation**: Professional PDF reports
- **Structured Data**: JSON-compatible data structures for further processing

### 🖥️ User Interfaces
- **Web Interface**: Modern Flask-based web application (http://localhost:5001)
- **CLI Tool**: Command-line interface for automation and scripting
- **Mac Apps**: Native macOS launcher apps for easy start/stop

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Google Custom Search API credentials
- macOS (for Mac app launchers, optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jwestphal31/demo-prep.git
   cd demo-prep
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements_web.txt
   ```

3. **Set up Google API credentials**

   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your credentials:
   ```
   GOOGLE_API_KEY=your_api_key_here
   GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here
   ```

   See [docs/SETUP.md](docs/SETUP.md) for detailed instructions on obtaining API credentials.

### Usage

#### Option 1: Web Interface (Recommended)

Start the web server:
```bash
python3 web_app.py
```

Or use the Mac apps (in `apps/` folder):
- Double-click **"Start Demo Prep.app"** to launch
- Double-click **"Stop Demo Prep.app"** to stop

Open your browser to: http://localhost:5001

#### Option 2: Command Line

```bash
python3 demo_prep.py example.com --company-name "Company Name"
```

**Example:**
```bash
python3 demo_prep.py anthropic.com --company-name "Anthropic"
```

## 📖 Documentation

- **[Setup Guide](docs/SETUP.md)** - Detailed setup instructions including Google API configuration
- **[Verification Guide](docs/VERIFICATION_GUIDE.md)** - How the company verification workflow works
- **[Launcher Guide](docs/LAUNCHER_GUIDE.md)** - Using the Mac app launchers

## 🏗️ Project Structure

```
demo-prep-tool/
├── demo_prep.py              # Core CLI tool
├── web_app.py                # Flask web application
├── security_vendors.py       # List of security vendors to check
├── requirements.txt          # Python dependencies (core)
├── requirements_web.txt      # Python dependencies (web interface)
├── .env.example              # Example environment variables
├── templates/
│   └── index.html            # Web interface template
├── docs/                     # Documentation
│   ├── SETUP.md
│   ├── VERIFICATION_GUIDE.md
│   └── LAUNCHER_GUIDE.md
├── scripts/                  # Helper scripts
│   ├── start_server.sh       # Start web server script
│   ├── stop_server.sh        # Stop web server script
│   ├── convert_to_pdf.py     # Markdown to PDF converter
│   ├── create_icons.py       # Mac app icon generator
│   └── batch_research.sh     # Batch research automation
└── apps/                     # Mac applications
    ├── Start Demo Prep.app
    └── Stop Demo Prep.app
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with your API credentials:

```bash
GOOGLE_API_KEY=your_google_api_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
```

### Google Custom Search API

This tool requires a Google Custom Search API key and Search Engine ID:

1. **API Key**: Get from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. **Search Engine ID**: Create at [Programmable Search Engine](https://programmablesearchengine.google.com/)

**Free Tier**: 100 searches per day
**Paid Tier**: $5 per 1,000 additional queries

See [docs/SETUP.md](docs/SETUP.md) for detailed setup instructions.

## 💡 Usage Examples

### Web Interface Workflow

1. Enter company domain (e.g., `epic.com`)
2. Optionally add company name and context
3. Add contact leads (name, title, email) - optional
4. Click "Start Research"
5. Verify the company information
6. Click "Yes, Continue" to begin deep research
7. View results and download reports

### CLI Examples

**Basic research:**
```bash
python3 demo_prep.py salesforce.com
```

**With company name:**
```bash
python3 demo_prep.py epic.com --company-name "Epic Systems"
```

**With context for better search accuracy:**
```bash
python3 demo_prep.py epic.com --company-name "Epic Systems" --company-context "healthcare software, Verona Wisconsin"
```

**Skip verification (for automation):**
```bash
python3 demo_prep.py anthropic.com --skip-verification
```

## 📊 API Quota Usage

Approximate Google Custom Search API queries per research:

- Company information: ~10 queries
- Technology stack: ~24 queries
- Security vendors: ~40 queries
- Security leadership: ~12 queries
- Executive leadership: ~12 queries
- Contact leads: ~1 query per contact

**Total**: ~100-150 queries per company (varies based on search results)

## 🔒 Security & Privacy

- Only uses publicly available information
- No data storage - results saved locally as markdown/PDF
- API keys stored in `.env` (gitignored)
- LinkedIn searches respect robots.txt and terms of service

## 🛠️ Development

### Running Tests

```bash
python3 demo_prep.py anthropic.com --company-name "Anthropic"
```

### Project Dependencies

**Core dependencies** (`requirements.txt`):
- `requests` - HTTP library
- `beautifulsoup4` - Web scraping

**Web interface dependencies** (`requirements_web.txt`):
- `flask` - Web framework
- `reportlab` - PDF generation
- `markdown` - Markdown processing

## 🤝 Contributing

This is a personal project, but suggestions and feedback are welcome! Feel free to open issues for bugs or feature requests.

## 📝 License

This project is for personal and educational use.

## 🙏 Acknowledgments

Built with assistance from Claude Code by Anthropic.

## 📬 Contact

GitHub: [@jwestphal31](https://github.com/jwestphal31)

---

**Note**: This tool is designed for legitimate business research and demo preparation. Please respect privacy and use responsibly.
