#!/bin/bash
# Demo Prep Tool - Stop Server Script

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Check if PID file exists
if [ ! -f "$DIR/.server.pid" ]; then
    osascript -e 'display notification "Server is not running" with title "Demo Prep Tool"'
    exit 0
fi

# Read PID
PID=$(cat "$DIR/.server.pid")

# Check if process is running
if ps -p $PID > /dev/null 2>&1; then
    # Kill the process
    kill $PID
    sleep 1

    # Force kill if still running
    if ps -p $PID > /dev/null 2>&1; then
        kill -9 $PID
    fi

    # Remove PID file
    rm -f "$DIR/.server.pid"

    osascript -e 'display notification "Server stopped successfully" with title "Demo Prep Tool" sound name "Glass"'
else
    # Process not running, just clean up
    rm -f "$DIR/.server.pid"
    osascript -e 'display notification "Server was not running" with title "Demo Prep Tool"'
fi
