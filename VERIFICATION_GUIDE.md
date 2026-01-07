# Company Verification Feature

## Overview

The tool now verifies you're researching the correct company before spending API quota on deep research.

## How It Works

### Step 1: Initial Research
The tool first gathers basic information:
- Website title and description
- LinkedIn profile
- Crunchbase info

### Step 2: Verification Prompt
You'll see something like this:

```
============================================================
COMPANY VERIFICATION
============================================================

📋 Information gathered for: Epic
🌐 Domain: epic.com

📄 Website Title: Epic | ...With the patient at the heart
📝 Description: Founded in a basement in 1979, Epic develops software
                to help people get well...

💼 LinkedIn: https://www.linkedin.com/company/epic1979
   Founded in a basement in 1979, Epic develops software to help
   people get well, stay well...

------------------------------------------------------------
❓ Is this the correct company you want to research?
------------------------------------------------------------

Enter (y)es to continue, (n)o to abort, or (c)ontext to add context:
```

### Step 3: Your Options

**Option 1: Confirm (y/yes)**
```
> y
✓ Continuing research...
```
Proceeds with full research (tech stack, security tools, vendors).

**Option 2: Abort (n/no)**
```
> n
✗ Research aborted.
```
Stops immediately, saves API quota.

**Option 3: Add Context (c/context)**
```
> c

Enter additional context (e.g., 'healthcare software', 'Verona Wisconsin'): healthcare EHR Verona
✓ Context added: healthcare EHR Verona

Updated search will use this context for better results.

❓ Continue with research?
> y
✓ Continuing research...
```
Adds context to refine searches, then continues.

## Usage Examples

### Interactive Mode (Default)
```bash
./run_demo_prep.sh epic.com
```
- Shows verification prompt
- You confirm or abort
- Great for manual research

### Automation Mode (Skip Verification)
```bash
./run_demo_prep.sh epic.com --skip-verification
```
- No prompt, runs automatically
- Great for batch processing
- Use when you're confident about the domain

### Pre-specify Company Details
```bash
./run_demo_prep.sh epic.com \
  --company-name "Epic Systems" \
  --company-context "healthcare software Verona Wisconsin"
```
- Shows verification with your provided details
- Context helps narrow down searches
- Best for ambiguous company names

### Full Automation with Context
```bash
./run_demo_prep.sh epic.com \
  --company-name "Epic Systems" \
  --company-context "healthcare software" \
  --skip-verification \
  -o epic_report.md
```
- No prompts, full context provided
- Perfect for scripts and automation

## When to Use Each Mode

### Use Interactive Mode When:
- Researching a company you're not familiar with
- Domain might be ambiguous (like "epic.com")
- Want to verify before using API quota
- Doing manual one-off research

### Use Skip Verification When:
- Batch processing multiple companies
- Running automated scripts
- Very confident about the domain
- Cost/quota is not a concern

### Add Context When:
- Company name is generic (Epic, Apple, Meta)
- Want more targeted results
- Know specific details (location, industry)
- Previous results showed wrong company

## Examples of Ambiguous Domains

These domains benefit from verification:

- **epic.com** - Epic Systems (healthcare) vs Epic Games (gaming)
- **meta.com** - Meta Platforms (Facebook) vs other "Meta" companies
- **apple.com** - Apple Inc. vs Apple Records
- **amazon.com** - Amazon.com (retail) vs AWS focus
- **toast.com** - Toast POS (restaurant) vs other Toast companies

## API Quota Savings

**Without Verification:**
- Immediate deep research
- ~40-50 search queries
- Might research wrong company

**With Verification:**
- Initial research: ~10-15 queries
- User confirms
- Deep research: ~35-40 queries
- **Saves quota if wrong company detected**

## Tips

1. **Always review the description** - It's the quickest way to confirm
2. **Check the LinkedIn URL** - Company LinkedIn IDs are usually unique
3. **Add context for better results** - Especially for tech stack and vendor searches
4. **Use --company-name for ambiguous domains** - Helps from the start

## Integration with Batch Scripts

```bash
#!/bin/bash
# Smart batch processing

companies=(
    "salesforce.com:Salesforce:CRM software"
    "epic.com:Epic Systems:healthcare EHR"
    "snowflake.com:Snowflake:data warehouse"
)

for entry in "${companies[@]}"; do
    IFS=':' read -r domain name context <<< "$entry"

    ./run_demo_prep.sh "$domain" \
        --company-name "$name" \
        --company-context "$context" \
        --skip-verification \
        -o "${domain%%.*}_report.md"
done
```

This way you can automate while still being precise about which companies you're researching.
