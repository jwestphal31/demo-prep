#!/bin/bash
# Batch research multiple companies

companies=(
    "salesforce.com"
    "snowflake.com"
    "datadog.com"
    "stripe.com"
)

for company in "${companies[@]}"; do
    echo "Researching $company..."
    ./run_demo_prep.sh "$company"

    # Generate PDF
    company_name="${company%%.*}"
    python3 convert_to_pdf.py "${company_name}_demo_prep.md" "${company_name}_report.pdf"

    echo "✓ Completed $company"
    echo "---"

    # Sleep to avoid rate limiting
    sleep 5
done

echo "All companies researched!"
