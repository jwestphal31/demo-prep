# Demo Prep Tool

A Python CLI tool that generates demo preparation documents by researching companies using web search and scraping.

## Features

- **Web Scraping**: Extracts basic information from company websites
- **Web Search Integration**: Searches LinkedIn, Crunchbase, and general web for company info
- **Tech Stack Discovery**: Automatically identifies technologies used by the company
- **Security Tools Detection**: Finds security tools and compliance information
- **Markdown Output**: Generates professionally formatted markdown documents
- **Google Docs Integration**: (Coming soon)

## Installation

1. Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

2. (Optional but recommended) Configure web search for enhanced research:
   - See [SETUP.md](SETUP.md) for detailed Google Custom Search API setup
   - The tool works without web search but provides basic website scraping only

## Usage

### Interactive Mode (Recommended)

Verifies you're researching the correct company:

```bash
./run_demo_prep.sh example.com
```

The tool will:
1. Gather initial company information
2. Show you what it found
3. Ask you to confirm before deep research

### Automation Mode

For batch processing or when you're confident:

```bash
./run_demo_prep.sh example.com --skip-verification
```

### With Company Context

For ambiguous company names (like "Epic"):

```bash
./run_demo_prep.sh epic.com \
  --company-name "Epic Systems" \
  --company-context "healthcare software Verona"
```

### Examples

**Basic interactive usage:**
```bash
./run_demo_prep.sh anthropic.com
```

**Skip verification for automation:**
```bash
./run_demo_prep.sh stripe.com --skip-verification -o stripe_demo.md
```

**Specify company details:**
```bash
./run_demo_prep.sh epic.com \
  --company-name "Epic Systems" \
  --company-context "healthcare EHR"
```

**Full automation:**
```bash
./run_demo_prep.sh salesforce.com \
  --company-name "Salesforce" \
  --company-context "CRM software" \
  --skip-verification
```

See [VERIFICATION_GUIDE.md](VERIFICATION_GUIDE.md) for detailed verification documentation.

## Output

The tool generates a markdown file with the following sections:

### Basic Mode (No Web Search)
- **Company Overview**: Website title, meta description, about text
- Placeholder sections for other features

### Enhanced Mode (With Web Search)
- **Company Overview**: Website title, meta description, about text
- **Company Information**:
  - LinkedIn profile with URL and snippet
  - Crunchbase profile with URL and snippet
  - Additional web references
  - Recent news articles
- **Technology Stack**:
  - Detected technologies (Python, React, AWS, etc.)
  - Source URLs for verification
  - Context snippets
- **Security Tools**:
  - Security tools and practices
  - Compliance information (SOC2, ISO 27001, etc.)
  - Source URLs and context
- **Competitive Battle Cards**: (Integration planned)

## Roadmap

- [x] Basic CLI interface
- [x] Website scraping
- [x] Markdown output
- [x] Web search integration with Google Custom Search API
- [x] LinkedIn profile discovery
- [x] Crunchbase profile discovery
- [x] Tech stack detection
- [x] Security tools detection
- [ ] Battle card knowledge base integration
- [ ] Google Docs API integration
- [ ] Caching layer for API optimization
- [ ] Support for alternative search providers

## Requirements

- Python 3.7+
- requests
- beautifulsoup4

## Web Search Integration

The tool uses Google Custom Search API to gather comprehensive information:

- **Company profiles**: Automatically finds LinkedIn and Crunchbase pages
- **Tech stack**: Searches engineering blogs, job postings, and tech articles
- **Security**: Discovers compliance certifications and security practices
- **News**: Pulls recent company news and announcements

**Cost**: Free tier includes 100 searches/day. Each company uses ~15-20 searches.

See [SETUP.md](SETUP.md) for configuration instructions.

## Future Enhancements

1. **Battle Cards**: Local knowledge base system for competitive intelligence
2. **Google Docs**: Automatic document creation in Google Docs
3. **Caching**: Cache research data to avoid redundant API lookups
4. **Templates**: Customizable document templates
5. **Batch Processing**: Research multiple companies in one run
6. **Alternative Search Providers**: Support for Bing, DuckDuckGo APIs
7. **Direct API Integrations**: LinkedIn API, Crunchbase API (when available)

## License

MIT
