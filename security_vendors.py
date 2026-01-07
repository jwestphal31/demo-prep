"""
Security vendor list for targeted searches
Based on common Black Hat sponsors and major security vendors
"""

# Major security vendors (typical Black Hat sponsors)
SECURITY_VENDORS = [
    # Endpoint Security / EDR
    "CrowdStrike",
    "SentinelOne",
    "Carbon Black",
    "Cylance",
    "Microsoft Defender",
    "Symantec",
    "McAfee",
    "Trend Micro",
    "Sophos",

    # SIEM / Security Analytics
    "Splunk",
    "IBM QRadar",
    "LogRhythm",
    "ArcSight",
    "Sumo Logic",
    "Elastic Security",
    "Azure Sentinel",

    # Identity & Access Management
    "CyberArk",
    "Okta",
    "Ping Identity",
    "ForgeRock",
    "BeyondTrust",
    "Auth0",
    "Duo Security",

    # Network Security
    "Palo Alto Networks",
    "Fortinet",
    "Cisco",
    "Check Point",
    "Zscaler",
    "F5 Networks",

    # Cloud Security
    "Wiz",
    "Lacework",
    "Prisma Cloud",
    "Orca Security",
    "Aqua Security",

    # Application Security
    "Snyk",
    "Veracode",
    "Checkmarx",
    "Fortify",
    "Qualys",

    # Vulnerability Management
    "Tenable",
    "Rapid7",
    "Nessus",

    # Email Security
    "Proofpoint",
    "Mimecast",
    "Barracuda",

    # Threat Intelligence
    "Recorded Future",
    "Mandiant",
    "CrowdStrike Threat Intelligence",
    "Anomali",

    # SOAR
    "Palo Alto Cortex",
    "Splunk SOAR",
    "IBM Resilient",

    # DLP
    "Varonis",
    "Digital Guardian",
    "Forcepoint",

    # CASB
    "Netskope",
    "McAfee MVISION",

    # Additional Major Vendors
    "Cloudflare",
    "Akamai",
    "FireEye",
    "Darktrace",
    "SonicWall",
]


def get_security_vendors():
    """Return the list of security vendors"""
    return SECURITY_VENDORS


def add_vendor(vendor_name):
    """Add a new vendor to the list"""
    if vendor_name not in SECURITY_VENDORS:
        SECURITY_VENDORS.append(vendor_name)
        return True
    return False
