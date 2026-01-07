#!/usr/bin/env python3
"""
Demo Prep Tool - Generate demo preparation documents by researching companies
"""

import argparse
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os
import sys
import re
from urllib.parse import urlparse, quote
from typing import List, Dict, Optional
from security_vendors import get_security_vendors


class WebSearcher:
    """Handle web search queries using Google Custom Search API"""

    def __init__(self, api_key: Optional[str] = None, search_engine_id: Optional[str] = None):
        """
        Initialize web searcher with API credentials

        Get credentials from:
        1. Google Cloud Console: https://console.cloud.google.com/
        2. Enable Custom Search API
        3. Create credentials (API key)
        4. Create a Custom Search Engine: https://programmablesearchengine.google.com/
        """
        self.api_key = api_key or os.environ.get('GOOGLE_API_KEY')
        self.search_engine_id = search_engine_id or os.environ.get('GOOGLE_SEARCH_ENGINE_ID')
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    def search(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Perform a web search and return results

        Args:
            query: Search query string
            num_results: Number of results to return (max 10)

        Returns:
            List of search result dictionaries with 'title', 'link', 'snippet'
        """
        if not self.api_key or not self.search_engine_id:
            print("⚠ Web search disabled: API credentials not configured")
            print("  Set GOOGLE_API_KEY and GOOGLE_SEARCH_ENGINE_ID environment variables")
            return []

        try:
            params = {
                'key': self.api_key,
                'cx': self.search_engine_id,
                'q': query,
                'num': min(num_results, 10)
            }

            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            results = []
            for item in data.get('items', []):
                results.append({
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', '')
                })

            return results

        except requests.exceptions.RequestException as e:
            print(f"⚠ Search error: {str(e)}")
            return []
        except Exception as e:
            print(f"⚠ Unexpected error during search: {str(e)}")
            return []

    def search_company_info(self, company_name: str, domain: str) -> Dict:
        """Search for general company information"""
        info = {
            'linkedin': None,
            'crunchbase': None,
            'about': [],
            'news': []
        }

        # Search for LinkedIn profile
        linkedin_query = f"{company_name} site:linkedin.com/company"
        linkedin_results = self.search(linkedin_query, num_results=3)
        for result in linkedin_results:
            if 'linkedin.com/company' in result['link']:
                info['linkedin'] = {
                    'url': result['link'],
                    'snippet': result['snippet']
                }
                break

        # Search for Crunchbase profile
        crunchbase_query = f"{company_name} site:crunchbase.com"
        crunchbase_results = self.search(crunchbase_query, num_results=3)
        for result in crunchbase_results:
            if 'crunchbase.com' in result['link']:
                info['crunchbase'] = {
                    'url': result['link'],
                    'snippet': result['snippet']
                }
                break

        # General company information
        general_query = f"{company_name} {domain} company about"
        general_results = self.search(general_query, num_results=5)
        for result in general_results:
            info['about'].append({
                'title': result['title'],
                'snippet': result['snippet'],
                'url': result['link']
            })

        # Recent news
        news_query = f"{company_name} news 2026"
        news_results = self.search(news_query, num_results=3)
        for result in news_results:
            info['news'].append({
                'title': result['title'],
                'snippet': result['snippet'],
                'url': result['link']
            })

        return info

    def search_tech_stack(self, company_name: str, domain: str) -> List[str]:
        """Search for company's technology stack"""
        tech_stack = []

        # Search for tech stack information with focus on job postings
        queries = [
            # Job posting searches (most reliable)
            f'site:linkedin.com/jobs "{company_name}" software engineer',
            f'site:glassdoor.com "{company_name}" developer',
            f'site:indeed.com "{company_name}" programmer',
            f'"{company_name}" careers software requirements',
            # General tech stack searches
            f'"{company_name}" tech stack',
            f'site:stackshare.io "{company_name}"',
            f'{domain} built with',
            # Discussion forums
            f'site:reddit.com "{company_name}" technologies',
        ]

        seen_techs = set()

        for query in queries:
            results = self.search(query, num_results=3)
            for result in results:
                # Extract potential technologies from snippets
                text = f"{result['title']} {result['snippet']}"
                techs = self._extract_technologies(text)
                for tech in techs:
                    if tech.lower() not in seen_techs:
                        seen_techs.add(tech.lower())
                        tech_stack.append({
                            'technology': tech,
                            'source': result['link'],
                            'context': result['snippet'][:200]
                        })

        return tech_stack

    def search_security_tools(self, company_name: str, domain: str) -> List[str]:
        """Search for company's security tools and practices"""
        security_tools = []

        # Search for actual security products with targeted queries
        queries = [
            # Security-specific job postings (most likely to mention tools)
            f'site:linkedin.com/jobs "{company_name}" "SOC analyst"',
            f'site:linkedin.com/jobs "{company_name}" "security operations"',
            f'site:indeed.com "{company_name}" SIEM OR Splunk OR CrowdStrike',
            f'"{company_name}" careers "security engineer" tools experience',
            # Vendor case studies and customer stories
            f'site:crowdstrike.com "{company_name}"',
            f'site:splunk.com customer "{company_name}"',
            f'site:okta.com "{company_name}"',
            f'site:paloaltonetworks.com "{company_name}"',
            # LinkedIn employee profiles (security staff list tools)
            f'site:linkedin.com "{company_name}" "security engineer" Splunk OR CrowdStrike',
            f'site:linkedin.com "{company_name}" SOC analyst tools',
            # Partnership announcements
            f'"{company_name}" partnership security OR deploys OR implements',
            f'"{company_name}" selects security solution',
            # Tech communities discussing tools
            f'site:reddit.com "{company_name}" security tools',
            # Official security pages (for compliance context)
            f'site:{domain} security',
        ]

        seen_tools = set()

        for query in queries:
            results = self.search(query, num_results=3)
            for result in results:
                # Extract security-related information
                text = f"{result['title']} {result['snippet']}"
                tools = self._extract_security_tools(text)
                for tool in tools:
                    if tool.lower() not in seen_tools:
                        seen_tools.add(tool.lower())
                        security_tools.append({
                            'tool': tool,
                            'source': result['link'],
                            'context': result['snippet'][:200]
                        })

        return security_tools

    def search_security_vendor_connections(self, company_name: str, domain: str) -> List[Dict]:
        """
        Search for connections between company and known security vendors
        Uses a curated list of security vendors (Black Hat sponsors, major vendors)
        """
        vendor_connections = []
        seen_vendors = set()

        # Get list of security vendors
        security_vendors = get_security_vendors()

        print(f"  🔍 Checking {len(security_vendors)} security vendors...")

        # Search for top vendors (limit to avoid quota exhaustion)
        # Prioritize the most common vendors
        priority_vendors = [
            "CrowdStrike", "Splunk", "CyberArk", "Okta", "Palo Alto Networks",
            "Fortinet", "Proofpoint", "Tenable", "Rapid7", "SentinelOne",
            "Wiz", "Zscaler", "Mimecast", "Varonis", "Recorded Future"
        ]

        vendors_to_check = priority_vendors + [v for v in security_vendors if v not in priority_vendors]

        # Check top 20 vendors to balance thoroughness with API quota
        for vendor in vendors_to_check[:20]:
            vendor_lower = vendor.lower()
            if vendor_lower in seen_vendors:
                continue

            # Search for company + vendor connection
            query = f'"{company_name}" "{vendor}"'
            results = self.search(query, num_results=2)

            for result in results:
                # Check if result actually mentions both company and vendor
                text = f"{result['title']} {result['snippet']}".lower()
                if company_name.lower() in text and vendor_lower in text:
                    seen_vendors.add(vendor_lower)
                    vendor_connections.append({
                        'vendor': vendor,
                        'source': result['link'],
                        'context': result['snippet'][:250],
                        'title': result['title']
                    })
                    break  # Found connection, move to next vendor

        return vendor_connections

    def _extract_technologies(self, text: str) -> List[str]:
        """Extract technology names from text"""
        # Common technologies to look for (expanded for job postings)
        tech_patterns = [
            # Programming languages
            r'\b(Python|Java|JavaScript|TypeScript|Go|Golang|Rust|Ruby|PHP|C\+\+|C#|\.NET|Swift|Kotlin|Scala|Perl|Objective-C|Visual Basic|VB\.NET)\b',
            # Web frameworks
            r'\b(React|Angular|Vue\.js|Vue|Django|Flask|FastAPI|Rails|Ruby on Rails|Spring Boot|Spring|Express|Next\.js|Node\.js|ASP\.NET|Laravel)\b',
            # Mobile
            r'\b(React Native|Flutter|Xamarin|Ionic|SwiftUI)\b',
            # Databases
            r'\b(PostgreSQL|Postgres|MySQL|SQL Server|MSSQL|MongoDB|Redis|Elasticsearch|DynamoDB|Cassandra|Oracle|DB2|MariaDB|SQLite|Couchbase|Neo4j)\b',
            # Specialized databases
            r'\b(InterSystems Cache|Caché|MUMPS|M technology)\b',
            # Cloud/Infrastructure
            r'\b(AWS|Amazon Web Services|Azure|Microsoft Azure|Google Cloud|GCP|Kubernetes|K8s|Docker|Terraform|Ansible|Chef|Puppet|CloudFormation)\b',
            # CI/CD & DevOps
            r'\b(Jenkins|GitLab CI|GitHub Actions|CircleCI|Travis CI|TeamCity|Bamboo|Bitbucket)\b',
            # Message queues & streaming
            r'\b(Kafka|RabbitMQ|ActiveMQ|Redis Queue|SQS|Kinesis|Apache Flink|Storm)\b',
            # APIs & Integration
            r'\b(GraphQL|REST API|SOAP|gRPC|Microservices|FHIR|HL7)\b',
            # Frontend tools
            r'\b(Webpack|Vite|Babel|TypeScript|jQuery|Bootstrap|Tailwind CSS|Material UI|Redux|MobX)\b',
            # Testing
            r'\b(Jest|Mocha|Pytest|JUnit|Selenium|Cypress|TestNG|Cucumber)\b',
            # Version control
            r'\b(Git|GitHub|GitLab|Bitbucket|SVN|Subversion|Mercurial)\b',
            # Other tools
            r'\b(Linux|Unix|Windows Server|Apache|Nginx|Tomcat|IIS|Maven|Gradle|npm|pip)\b'
        ]

        technologies = []
        for pattern in tech_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                tech = match.group(0)
                if tech not in technologies:
                    technologies.append(tech)

        return technologies

    def _extract_security_tools(self, text: str) -> List[str]:
        """Extract security tool names from text"""
        # Common security tools to look for (expanded with specific products)
        security_patterns = [
            # SIEM/Monitoring platforms
            r'\b(Splunk|Splunk Enterprise|Datadog|New Relic|Sumo Logic|ELK Stack|Elastic|Elasticsearch|LogRhythm|QRadar|IBM QRadar|ArcSight|HP ArcSight)\b',
            # Identity & Access Management (PAM)
            r'\b(CyberArk|Okta|Auth0|Azure AD|Active Directory|Ping Identity|OneLogin|Duo Security|Duo|ForgeRock|BeyondTrust|Thycotic|Centrify)\b',
            # Endpoint Security (EDR/EPP)
            r'\b(CrowdStrike|CrowdStrike Falcon|Carbon Black|VMware Carbon Black|SentinelOne|Cylance|Symantec|Symantec Endpoint|McAfee|Trend Micro|Sophos|Microsoft Defender)\b',
            # Network Security
            r'\b(Palo Alto|Palo Alto Networks|Fortinet|FortiGate|Cisco ASA|Cisco Firepower|Check Point|F5 Networks|F5|Barracuda|Zscaler|Cisco Umbrella)\b',
            # Cloud Security
            r'\b(Cloudflare|Akamai|AWS GuardDuty|AWS Security Hub|Azure Security Center|Azure Sentinel|Google Cloud Security|Prisma Cloud|Wiz|Lacework)\b',
            # Application Security (SAST/DAST)
            r'\b(Snyk|Veracode|Checkmarx|SonarQube|WhiteSource|Mend|Black Duck|Fortify|HP Fortify|Qualys|Aqua Security|Twistlock)\b',
            # Vulnerability Management
            r'\b(Nessus|Tenable Nessus|Rapid7|InsightVM|Tenable\.io|OpenVAS|Nexpose|Qualys VMDR)\b',
            # Email Security
            r'\b(Proofpoint|Mimecast|Barracuda Email Security|Microsoft Defender for Office|Cisco Email Security)\b',
            # Threat Intelligence
            r'\b(Recorded Future|ThreatConnect|Anomali|CrowdStrike Threat Intelligence|Mandiant|FireEye)\b',
            # CASB (Cloud Access Security Broker)
            r'\b(Netskope|McAfee MVISION|Symantec CloudSOC|Microsoft Cloud App Security)\b',
            # Security Automation (SOAR)
            r'\b(Palo Alto Cortex XSOAR|Splunk SOAR|Phantom|IBM Resilient|Swimlane|Demisto)\b',
            # Compliance Standards
            r'\b(SOC ?2|SOC2 Type II|ISO 27001|ISO27001|HIPAA|HITECH|GDPR|PCI DSS|PCI-DSS|FedRAMP|NIST|CCPA)\b',
            # Security Practices
            r'\b(WAF|Web Application Firewall|Firewall|IDS|IPS|SIEM|VPN|MFA|Multi-Factor|SSO|Single Sign-On|Zero Trust|Penetration Testing|Pen Test|Red Team|Blue Team)\b',
            # Encryption & PKI
            r'\b(TLS|SSL|AES|RSA|PKI|Certificate Authority|HSM|Hardware Security Module)\b',
            # Security Frameworks
            r'\b(OWASP|CIS Controls|NIST CSF|MITRE ATT&CK)\b',
            # DLP & Data Security
            r'\b(DLP|Data Loss Prevention|Varonis|Digital Guardian|Forcepoint DLP)\b',
            # Incident Response
            r'\b(PagerDuty|ServiceNow Security Operations|Jira Service Management)\b'
        ]

        tools = []
        for pattern in security_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                tool = match.group(0)
                if tool not in tools:
                    tools.append(tool)

        return tools

    def search_stakeholders(self, company_name: str, role_titles: list, category: str) -> list:
        """
        Search for company stakeholders by role titles

        Args:
            company_name: Company name to search for
            role_titles: List of role titles to search (e.g., ["CISO", "VP Security"])
            category: Category label (e.g., "Security Leadership")

        Returns:
            List of dictionaries with name, title, linkedin_url, role_category
        """
        stakeholders = []
        seen_urls = set()

        for role_title in role_titles:
            # Search LinkedIn for this role
            query = f'site:linkedin.com/in "{company_name}" "{role_title}"'
            results = self.search(query, num_results=2)

            for result in results:
                # Extract LinkedIn URL
                linkedin_url = self._extract_linkedin_url(result['link'])
                if not linkedin_url:
                    continue

                # Normalize and check for duplicates
                normalized_url = self._normalize_linkedin_url(linkedin_url)
                if normalized_url in seen_urls:
                    continue
                seen_urls.add(normalized_url)

                # Extract name and title
                name = self._extract_name_from_title(result['title'])
                title = self._extract_title_from_result(result['title'], result['snippet'])

                if name and linkedin_url:
                    stakeholders.append({
                        'name': name,
                        'title': title or role_title,  # Fallback to searched role
                        'linkedin_url': linkedin_url,
                        'role_category': category
                    })

            # Early termination: if we found someone for this role category,
            # we can be less aggressive searching variants
            if len(stakeholders) >= 2:
                break

        return stakeholders

    def _extract_linkedin_url(self, url_or_text: str) -> Optional[str]:
        """Extract LinkedIn profile URL"""
        pattern = r'https?://(?:www\.)?linkedin\.com/in/[\w\-]+'
        match = re.search(pattern, url_or_text)
        return match.group(0) if match else None

    def _normalize_linkedin_url(self, url: str) -> str:
        """Normalize LinkedIn URL for deduplication"""
        # Remove query parameters and trailing slashes
        clean_url = url.split('?')[0].rstrip('/')
        return clean_url.lower()

    def _extract_name_from_title(self, title: str) -> Optional[str]:
        """
        Extract person name from LinkedIn search result title
        Typical formats:
        - "FirstName LastName - Title at Company | LinkedIn"
        - "FirstName LastName | Professional Profile"
        """
        # Pattern: Everything before " - " or " | "
        pattern = r'^([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z\'\-]+){1,3})\s*[-–|]'
        match = re.search(pattern, title)
        if match:
            name = match.group(1).strip()
            # Filter out company names or generic terms
            if len(name.split()) >= 2 and 'LinkedIn' not in name:
                return name

        return None

    def _extract_title_from_result(self, title_text: str, snippet: str) -> Optional[str]:
        """Extract job title from search result"""
        # Pattern: extract text between "- " and "at Company" or "|"
        pattern = r'[-–]\s*([^|]+?)\s*(?:at\s+|\|)'
        match = re.search(pattern, title_text)
        if match:
            job_title = match.group(1).strip()
            if len(job_title) > 0 and 'LinkedIn' not in job_title:
                return job_title

        return None

    def search_contact_linkedin(self, contact_name: str, company_name: str, title: str = None) -> dict:
        """
        Search for a specific person's LinkedIn profile

        Args:
            contact_name: Person's full name
            company_name: Company they work at
            title: Optional job title to refine search

        Returns:
            Dict with linkedin_url and linkedin_snippet, or empty dict if not found
        """
        # Construct search query
        if title:
            query = f'site:linkedin.com/in "{contact_name}" "{company_name}" "{title}"'
        else:
            query = f'site:linkedin.com/in "{contact_name}" "{company_name}"'

        # Search LinkedIn
        results = self.search(query, num_results=1)

        if results:
            result = results[0]
            # Extract LinkedIn URL
            linkedin_url = self._extract_linkedin_url(result['link'])

            if linkedin_url:
                return {
                    'linkedin_url': linkedin_url,
                    'linkedin_snippet': result.get('snippet', '')
                }

        return {}


class CompanyResearcher:
    """Research company information from various sources"""

    def __init__(self, domain, web_searcher: Optional[WebSearcher] = None,
                 company_name_override: Optional[str] = None,
                 company_context: Optional[str] = None,
                 contact_leads: Optional[List[Dict]] = None):
        self.domain = domain
        self.company_name = company_name_override or self._extract_company_name(domain)
        self.company_context = company_context
        self.web_searcher = web_searcher
        self.data = {
            'domain': domain,
            'company_name': self.company_name,
            'company_context': company_context,
            'research_date': datetime.now().strftime('%Y-%m-%d'),
            'website_info': {},
            'tech_stack': [],
            'security_tools': [],
            'security_vendors': [],
            'company_info': {},
            'security_leadership': [],
            'executive_leadership': [],
            'contact_leads': contact_leads or [],
            'search_enabled': web_searcher is not None and web_searcher.api_key is not None
        }

    def _extract_company_name(self, domain):
        """Extract company name from domain"""
        # Remove common TLDs and clean up
        name = domain.replace('www.', '').split('.')[0]
        return name.title()

    def verify_company(self) -> bool:
        """
        Verify that we're researching the correct company
        Returns True to continue, False to abort
        """
        print("\n" + "=" * 60)
        print("COMPANY VERIFICATION")
        print("=" * 60)

        print(f"\n📋 Information gathered for: {self.company_name}")
        print(f"🌐 Domain: {self.domain}")

        if self.company_context:
            print(f"📍 Context: {self.company_context}")

        # Show website info if available
        if self.data.get('website_info'):
            info = self.data['website_info']
            if info.get('title'):
                print(f"\n📄 Website Title: {info['title']}")
            if info.get('description'):
                print(f"📝 Description: {info['description'][:150]}...")

        # Show LinkedIn info if available
        if self.data.get('company_info', {}).get('linkedin'):
            linkedin = self.data['company_info']['linkedin']
            print(f"\n💼 LinkedIn: {linkedin['url']}")
            print(f"   {linkedin['snippet'][:150]}...")

        print("\n" + "-" * 60)
        print("❓ Is this the correct company you want to research?")
        print("-" * 60)

        while True:
            response = input("\nEnter (y)es to continue, (n)o to abort, or (c)ontext to add context: ").lower().strip()

            if response in ['y', 'yes']:
                print("✓ Continuing research...\n")
                return True
            elif response in ['n', 'no']:
                print("✗ Research aborted.")
                return False
            elif response in ['c', 'context']:
                new_context = input("\nEnter additional context (e.g., 'healthcare software', 'Verona Wisconsin'): ").strip()
                if new_context:
                    self.company_context = new_context
                    self.data['company_context'] = new_context
                    print(f"✓ Context added: {new_context}")
                    print("\nUpdated search will use this context for better results.")
                    print("\n❓ Continue with research?")
            else:
                print("Please enter 'y', 'n', or 'c'")

    def research_website(self):
        """Scrape basic information from company website"""
        print(f"🔍 Researching {self.domain}...")

        try:
            url = f"https://{self.domain}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                self.data['website_info']['description'] = meta_desc.get('content', '')

            # Extract title
            title = soup.find('title')
            if title:
                self.data['website_info']['title'] = title.text.strip()

            # Look for common about/description text
            about_keywords = ['about', 'what we do', 'who we are']
            for keyword in about_keywords:
                about_section = soup.find(lambda tag: tag.name in ['p', 'div'] and
                                        keyword in tag.text.lower())
                if about_section:
                    self.data['website_info']['about'] = about_section.text.strip()[:500]
                    break

            print(f"✓ Website scraped successfully")

        except Exception as e:
            print(f"⚠ Error scraping website: {str(e)}")
            self.data['website_info']['error'] = str(e)

    def research_tech_stack(self):
        """Research company's tech stack"""
        print(f"🔍 Researching tech stack for {self.company_name}...")

        if not self.web_searcher or not self.web_searcher.api_key:
            self.data['tech_stack'] = []
            print(f"⚠ Skipping tech stack research - web search not configured")
            return

        try:
            tech_stack = self.web_searcher.search_tech_stack(self.company_name, self.domain)
            self.data['tech_stack'] = tech_stack
            print(f"✓ Found {len(tech_stack)} technologies")
        except Exception as e:
            print(f"⚠ Error researching tech stack: {str(e)}")
            self.data['tech_stack'] = []

    def research_security_tools(self):
        """Research company's security tools"""
        print(f"🔍 Researching security tools for {self.company_name}...")

        if not self.web_searcher or not self.web_searcher.api_key:
            self.data['security_tools'] = []
            print(f"⚠ Skipping security tools research - web search not configured")
            return

        try:
            security_tools = self.web_searcher.search_security_tools(self.company_name, self.domain)
            self.data['security_tools'] = security_tools
            print(f"✓ Found {len(security_tools)} security tools/practices")
        except Exception as e:
            print(f"⚠ Error researching security tools: {str(e)}")
            self.data['security_tools'] = []

    def research_security_vendors(self):
        """Research connections with known security vendors"""
        print(f"🔍 Checking security vendor connections for {self.company_name}...")

        if not self.web_searcher or not self.web_searcher.api_key:
            self.data['security_vendors'] = []
            print(f"⚠ Skipping vendor research - web search not configured")
            return

        try:
            vendor_connections = self.web_searcher.search_security_vendor_connections(
                self.company_name, self.domain
            )
            self.data['security_vendors'] = vendor_connections
            print(f"✓ Found {len(vendor_connections)} vendor connections")
        except Exception as e:
            print(f"⚠ Error researching security vendors: {str(e)}")
            self.data['security_vendors'] = []

    def get_company_info(self):
        """Get general company information"""
        print(f"🔍 Gathering company information for {self.company_name}...")

        if not self.web_searcher or not self.web_searcher.api_key:
            self.data['company_info'] = {}
            print(f"⚠ Skipping company info research - web search not configured")
            return

        try:
            company_info = self.web_searcher.search_company_info(self.company_name, self.domain)
            self.data['company_info'] = company_info

            # Print what was found
            found = []
            if company_info.get('linkedin'):
                found.append("LinkedIn")
            if company_info.get('crunchbase'):
                found.append("Crunchbase")
            if company_info.get('about'):
                found.append(f"{len(company_info['about'])} references")
            if company_info.get('news'):
                found.append(f"{len(company_info['news'])} news items")

            print(f"✓ Found: {', '.join(found) if found else 'limited info'}")
        except Exception as e:
            print(f"⚠ Error gathering company info: {str(e)}")
            self.data['company_info'] = {}

    def research_security_leadership(self):
        """Research security leadership roles"""
        print(f"🔍 Researching security leadership for {self.company_name}...")

        if not self.web_searcher or not self.web_searcher.api_key:
            self.data['security_leadership'] = []
            print(f"⚠ Skipping security leadership research - web search not configured")
            return

        try:
            security_roles = [
                "CISO",
                "Chief Information Security Officer",
                "VP Security",
                "Vice President of Security",
                "Director of Security",
                "Security Manager",
                "Chief Security Officer",
                "Head of Security"
            ]

            stakeholders = self.web_searcher.search_stakeholders(
                self.company_name,
                security_roles,
                "Security Leadership"
            )

            self.data['security_leadership'] = stakeholders
            print(f"✓ Found {len(stakeholders)} security leader(s)")
        except Exception as e:
            print(f"⚠ Error researching security leadership: {str(e)}")
            self.data['security_leadership'] = []

    def research_executive_leadership(self):
        """Research executive leadership roles"""
        print(f"🔍 Researching executive leadership for {self.company_name}...")

        if not self.web_searcher or not self.web_searcher.api_key:
            self.data['executive_leadership'] = []
            print(f"⚠ Skipping executive leadership research - web search not configured")
            return

        try:
            executive_roles = [
                "CEO",
                "Chief Executive Officer",
                "CTO",
                "Chief Technology Officer",
                "CFO",
                "Chief Financial Officer",
                "COO",
                "Chief Operating Officer",
                "CIO",
                "Chief Information Officer",
                "CPO",
                "Chief Product Officer"
            ]

            stakeholders = self.web_searcher.search_stakeholders(
                self.company_name,
                executive_roles,
                "Executive Leadership"
            )

            self.data['executive_leadership'] = stakeholders
            print(f"✓ Found {len(stakeholders)} executive(s)")
        except Exception as e:
            print(f"⚠ Error researching executive leadership: {str(e)}")
            self.data['executive_leadership'] = []

    def enrich_contact_leads(self):
        """Search LinkedIn for each contact lead to retrieve profile information"""
        if not self.data.get('contact_leads'):
            return

        print(f"🔍 Enriching contact leads with LinkedIn profiles...")

        if not self.web_searcher or not self.web_searcher.api_key:
            print(f"⚠ Skipping contact enrichment - web search not configured")
            for contact in self.data['contact_leads']:
                contact['search_performed'] = False
            return

        enriched_count = 0
        for contact in self.data['contact_leads']:
            try:
                # Search for LinkedIn profile
                linkedin_data = self.web_searcher.search_contact_linkedin(
                    contact['name'],
                    self.company_name,
                    contact.get('title')
                )

                # Merge LinkedIn data with user-provided data
                if linkedin_data:
                    contact['linkedin_url'] = linkedin_data.get('linkedin_url')
                    contact['linkedin_snippet'] = linkedin_data.get('linkedin_snippet')
                    contact['search_performed'] = True
                    enriched_count += 1
                else:
                    contact['linkedin_url'] = None
                    contact['linkedin_snippet'] = None
                    contact['search_performed'] = True

            except Exception as e:
                print(f"⚠ Error enriching contact {contact['name']}: {str(e)}")
                contact['search_performed'] = False

        print(f"✓ Enriched {enriched_count} of {len(self.data['contact_leads'])} contact(s)")


class MarkdownGenerator:
    """Generate markdown documents from research data"""

    @staticmethod
    def generate(data, output_path):
        """Generate a formatted markdown document"""
        print(f"📝 Generating markdown document...")

        md_content = []

        # Title
        md_content.append(f"# Demo Prep: {data['company_name']}")
        md_content.append(f"\n**Domain:** {data['domain']}")
        md_content.append(f"\n**Research Date:** {data['research_date']}")
        md_content.append("\n---\n")

        # Company Overview
        md_content.append("## Company Overview\n")
        if data['website_info']:
            if 'title' in data['website_info']:
                md_content.append(f"**Website Title:** {data['website_info']['title']}\n")
            if 'description' in data['website_info']:
                md_content.append(f"**Description:** {data['website_info']['description']}\n")
            if 'about' in data['website_info']:
                md_content.append(f"\n**About:**\n{data['website_info']['about']}\n")
            if 'error' in data['website_info']:
                md_content.append(f"\n*Note: Error accessing website - {data['website_info']['error']}*\n")

        # Company Information
        md_content.append("\n## Company Information\n")
        if data['company_info']:
            company_info = data['company_info']

            # LinkedIn
            if company_info.get('linkedin'):
                md_content.append(f"\n### LinkedIn Profile\n")
                md_content.append(f"**URL:** [{company_info['linkedin']['url']}]({company_info['linkedin']['url']})\n\n")
                md_content.append(f"{company_info['linkedin']['snippet']}\n")

            # Crunchbase
            if company_info.get('crunchbase'):
                md_content.append(f"\n### Crunchbase Profile\n")
                md_content.append(f"**URL:** [{company_info['crunchbase']['url']}]({company_info['crunchbase']['url']})\n\n")
                md_content.append(f"{company_info['crunchbase']['snippet']}\n")

            # About/Overview
            if company_info.get('about'):
                md_content.append(f"\n### Additional Information\n")
                for idx, item in enumerate(company_info['about'][:3], 1):
                    md_content.append(f"\n**Source {idx}:** [{item['title']}]({item['url']})\n")
                    md_content.append(f"{item['snippet']}\n")

            # Recent News
            if company_info.get('news'):
                md_content.append(f"\n### Recent News\n")
                for item in company_info['news']:
                    md_content.append(f"- [{item['title']}]({item['url']})\n")
                    md_content.append(f"  {item['snippet']}\n")

            if not any([company_info.get('linkedin'), company_info.get('crunchbase'),
                       company_info.get('about'), company_info.get('news')]):
                md_content.append("*No additional company information available*\n")
        else:
            md_content.append("*No additional company information available*\n")

        # Contact Leads
        md_content.append("\n## Contact Leads\n")
        if data.get('contact_leads') and len(data['contact_leads']) > 0:
            md_content.append("*Contacts to track for this demo preparation*\n\n")
            for contact in data['contact_leads']:
                md_content.append(f"### {contact['name']}\n")
                if contact.get('title'):
                    md_content.append(f"**Title:** {contact['title']}\n\n")
                if contact.get('email'):
                    md_content.append(f"**Email:** [{contact['email']}](mailto:{contact['email']})\n\n")
                if contact.get('linkedin_url'):
                    md_content.append(f"**LinkedIn:** [{contact['linkedin_url']}]({contact['linkedin_url']})\n\n")
                if contact.get('linkedin_snippet'):
                    md_content.append(f"*{contact['linkedin_snippet']}*\n\n")
                if not contact.get('title') and not contact.get('email') and not contact.get('linkedin_url'):
                    md_content.append("*No additional contact details*\n\n")
        else:
            md_content.append("*No contact leads added*\n")

        # Security Leadership
        md_content.append("\n## Security Leadership\n")
        if data.get('search_enabled') == False:
            md_content.append("*Web search not configured - enable search for stakeholder research*\n")
        elif data.get('security_leadership'):
            if len(data['security_leadership']) > 0:
                for person in data['security_leadership']:
                    md_content.append(f"\n### {person['name']}\n")
                    md_content.append(f"**Title:** {person['title']}\n\n")
                    md_content.append(f"**LinkedIn:** [{person['linkedin_url']}]({person['linkedin_url']})\n")
            else:
                md_content.append("*No security leadership information found*\n")
        else:
            md_content.append("*No security leadership information found*\n")

        # Executive Leadership
        md_content.append("\n## Executive Leadership\n")
        if data.get('search_enabled') == False:
            md_content.append("*Web search not configured - enable search for stakeholder research*\n")
        elif data.get('executive_leadership'):
            if len(data['executive_leadership']) > 0:
                for person in data['executive_leadership']:
                    md_content.append(f"\n### {person['name']}\n")
                    md_content.append(f"**Title:** {person['title']}\n\n")
                    md_content.append(f"**LinkedIn:** [{person['linkedin_url']}]({person['linkedin_url']})\n")
            else:
                md_content.append("*No executive leadership information found*\n")
        else:
            md_content.append("*No executive leadership information found*\n")

        # Tech Stack
        md_content.append("\n## Technology Stack\n")
        if data.get('search_enabled') == False:
            md_content.append("*Web search not configured - enable search for tech stack detection*\n")
        elif data['tech_stack']:
            seen = set()
            for item in data['tech_stack']:
                if isinstance(item, dict):
                    tech = item['technology']
                    if tech not in seen:
                        seen.add(tech)
                        md_content.append(f"- **{tech}**\n")
                        md_content.append(f"  - Source: {item['source']}\n")
                        if item.get('context'):
                            md_content.append(f"  - Context: {item['context']}\n")
                else:
                    md_content.append(f"- {item}\n")
        else:
            md_content.append("*No tech stack information found*\n")

        # Security Vendor Connections
        md_content.append("\n## Security Vendor Connections\n")
        md_content.append("*Verified connections with known security vendors*\n\n")
        if data.get('search_enabled') == False:
            md_content.append("*Web search not configured - enable search for vendor detection*\n")
        elif data.get('security_vendors'):
            vendors_found = data['security_vendors']
            if vendors_found:
                md_content.append(f"Found {len(vendors_found)} vendor connection(s):\n\n")
                for item in vendors_found:
                    md_content.append(f"### {item['vendor']}\n")
                    md_content.append(f"**Source:** [{item['title']}]({item['source']})\n\n")
                    md_content.append(f"**Context:** {item['context']}\n\n")
            else:
                md_content.append("*No vendor connections found*\n")
        else:
            md_content.append("*No vendor connections found*\n")

        # Battle Cards Section (placeholder for later)
        md_content.append("\n## Competitive Battle Cards\n")
        md_content.append("*Battle cards integration coming soon*\n")

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(''.join(md_content))

        print(f"✓ Document generated: {output_path}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Generate demo prep documents by researching companies',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python demo_prep.py example.com
  python demo_prep.py example.com -o output.md
        """
    )

    parser.add_argument(
        'domain',
        help='Company domain (e.g., example.com)'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output markdown file path (default: <company>_demo_prep.md)',
        default=None
    )

    parser.add_argument(
        '--company-name',
        help='Full company name for verification (e.g., "Epic Systems")',
        default=None
    )

    parser.add_argument(
        '--company-context',
        help='Additional context (e.g., "healthcare software", "Verona Wisconsin")',
        default=None
    )

    parser.add_argument(
        '--skip-verification',
        help='Skip company verification prompt',
        action='store_true',
        default=False
    )

    args = parser.parse_args()

    # Clean up domain input
    domain = args.domain.replace('https://', '').replace('http://', '').strip('/')

    # Set output path
    company_name = domain.replace('www.', '').split('.')[0]
    output_path = args.output or f"{company_name}_demo_prep.md"

    print("=" * 60)
    print("Demo Prep Tool")
    print("=" * 60)
    print(f"Company: {domain}")
    print(f"Output: {output_path}")
    print("=" * 60)
    print()

    # Initialize web searcher
    web_searcher = WebSearcher()
    if web_searcher.api_key:
        print("✓ Web search enabled")
    else:
        print("⚠ Web search disabled - set GOOGLE_API_KEY and GOOGLE_SEARCH_ENGINE_ID")
        print("  to enable LinkedIn, Crunchbase, tech stack, and security tools research")
    print()

    # Research company
    researcher = CompanyResearcher(
        domain,
        web_searcher=web_searcher,
        company_name_override=args.company_name,
        company_context=args.company_context
    )

    # Initial research
    researcher.research_website()
    researcher.get_company_info()

    # Verify company (unless skipped)
    if not args.skip_verification:
        if not researcher.verify_company():
            print("\n" + "=" * 60)
            print("Research aborted by user.")
            print("=" * 60)
            sys.exit(0)

    # Deep research
    print()
    researcher.research_tech_stack()
    researcher.research_security_vendors()
    researcher.research_security_leadership()
    researcher.research_executive_leadership()

    print()
    print("=" * 60)

    # Generate markdown document
    MarkdownGenerator.generate(researcher.data, output_path)

    print("=" * 60)
    print(f"✓ Complete! Open {output_path} to view the demo prep document.")
    print("=" * 60)


if __name__ == '__main__':
    main()
