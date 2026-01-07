# Company Verification Demo

## What We Built

Added an interactive verification step to confirm you're researching the correct company before using API quota.

## The Problem We Solved

**Before:**
```bash
$ ./run_demo_prep.sh epic.com
```
→ Immediately researches "Epic"
→ Might get Epic Games, Epic Books, Epic Systems mixed together
→ Uses 40-50 API queries before you realize it's wrong
→ Wastes time and quota

**After:**
```bash
$ ./run_demo_prep.sh epic.com

[Initial research happens - ~15 queries]

============================================================
COMPANY VERIFICATION
============================================================

📋 Information gathered for: Epic
🌐 Domain: epic.com

📄 Website Title: Epic | ...With the patient at the heart
📝 Description: Founded in a basement in 1979, Epic develops
                software to help people get well...

💼 LinkedIn: https://www.linkedin.com/company/epic1979
   Founded in a basement in 1979, Epic develops software...

❓ Is this the correct company you want to research?

Enter (y)es to continue, (n)o to abort, or (c)ontext to add context: y

[Deep research continues - ~35 more queries]
```

## Usage Modes

### 1. Interactive (Default)
```bash
./run_demo_prep.sh epic.com
```
- Shows what was found
- You confirm before proceeding
- Can add context if needed
- Saves quota if wrong company

### 2. With Pre-defined Context
```bash
./run_demo_prep.sh epic.com \
  --company-name "Epic Systems" \
  --company-context "healthcare software"
```
- Uses your provided name/context
- Still shows verification
- Better search results with context

### 3. Skip Verification (Automation)
```bash
./run_demo_prep.sh epic.com --skip-verification
```
- No prompts
- Runs automatically
- Good for batch processing

## Examples

### Example 1: Ambiguous Company Name

**Input:**
```bash
./run_demo_prep.sh meta.com
```

**Verification Shows:**
```
📋 Information gathered for: Meta
🌐 Domain: meta.com

📄 Website Title: Meta | Social metaverse company
📝 Description: Meta builds technologies that help people connect...

💼 LinkedIn: https://www.linkedin.com/company/meta
   Meta builds technologies to help people connect, find communities...
```

**Your Decision:**
- (y) - Correct, this is Facebook/Meta Platforms
- (n) - Wrong company, abort
- (c) - Add context like "Mark Zuckerberg" or "Facebook parent company"

### Example 2: Using Context from Start

**Input:**
```bash
./run_demo_prep.sh epic.com \
  --company-name "Epic Systems" \
  --company-context "healthcare EHR Verona Wisconsin"
```

**Result:**
- Tool knows to focus on healthcare company
- Searches specifically for "Epic Systems healthcare"
- Better vendor matches (Splunk for healthcare, CrowdStrike for Epic Systems)
- Less noise from Epic Games

### Example 3: Batch Processing

**Script:**
```bash
companies=(
    "salesforce.com:Salesforce:CRM"
    "epic.com:Epic Systems:healthcare"
    "stripe.com:Stripe:payments"
)

for entry in "${companies[@]}"; do
    IFS=':' read -r domain name context <<< "$entry"

    ./run_demo_prep.sh "$domain" \
        --company-name "$name" \
        --company-context "$context" \
        --skip-verification
done
```

**Result:**
- Processes all companies automatically
- Each has proper context
- No manual intervention needed
- Accurate, targeted results

## Benefits

### ✅ Accuracy
- Confirms correct company before deep research
- Reduces wrong results (Epic Games vs Epic Systems)

### ✅ Cost Savings
- Uses ~15 queries for initial check
- Abort if wrong = saves ~35 queries
- Important with 100/day free tier

### ✅ Flexibility
- Interactive for manual research
- Automated for batch processing
- Context for ambiguous names

### ✅ Better Results
- Context improves search targeting
- "Epic Systems healthcare" vs just "Epic"
- More relevant vendor connections

## Command Reference

### Full Command Options
```bash
./run_demo_prep.sh <domain> [options]

Options:
  -o, --output FILE              Output markdown file
  --company-name NAME            Full company name
  --company-context CONTEXT      Industry/location context
  --skip-verification            Skip confirmation prompt
```

### Common Patterns

**Research with confidence:**
```bash
./run_demo_prep.sh anthropic.com
# (verify when prompted)
```

**Batch automation:**
```bash
./run_demo_prep.sh *.com --skip-verification
```

**Disambiguate:**
```bash
./run_demo_prep.sh epic.com \
  --company-name "Epic Systems" \
  --company-context "healthcare"
```

**Full control:**
```bash
./run_demo_prep.sh example.com \
  --company-name "Example Corp" \
  --company-context "fintech startup" \
  --skip-verification \
  -o example_report.md
```

## Files Created

- `VERIFICATION_GUIDE.md` - Full documentation
- Updated `README.md` - Usage examples
- Updated `demo_prep.py` - New verification logic
- Updated `run_demo_prep.sh` - Helper script

## Try It!

```bash
# Interactive mode (will prompt)
./run_demo_prep.sh epic.com

# With context (better results)
./run_demo_prep.sh epic.com \
  --company-name "Epic Systems" \
  --company-context "healthcare software"
```
