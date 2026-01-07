#!/bin/bash
# Helper script to run demo prep tool with environment variables

export GOOGLE_API_KEY="AIzaSyApsXw8ARwjaZuK0KY8yQOcAJ0lDxq3PWU"
export GOOGLE_SEARCH_ENGINE_ID="764f936dfceea49e2"

# Usage examples:
# ./run_demo_prep.sh example.com
# ./run_demo_prep.sh example.com --company-name "Example Corp"
# ./run_demo_prep.sh example.com --company-context "healthcare software"
# ./run_demo_prep.sh example.com --skip-verification

python3 demo_prep.py "$@"
