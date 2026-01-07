#!/bin/bash
# Demo Prep Tool - Start Server Script

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Load environment variables
export GOOGLE_API_KEY="AIzaSyApsXw8ARwjaZuK0KY8yQOcAJ0lDxq3PWU"
export GOOGLE_SEARCH_ENGINE_ID="764f936dfceea49e2"

# Check if server is already running
if [ -f "$DIR/.server.pid" ]; then
    PID=$(cat "$DIR/.server.pid")
    if ps -p $PID > /dev/null 2>&1; then
        osascript -e 'display notification "Server is already running at http://localhost:5001" with title "Demo Prep Tool"'
        open http://localhost:5001
        exit 0
    fi
fi

# Start the server in the background
nohup python3 "$DIR/web_app.py" > "$DIR/server.log" 2>&1 &
SERVER_PID=$!

# Save the PID
echo $SERVER_PID > "$DIR/.server.pid"

# Wait a moment for server to start
sleep 2

# Check if server started successfully
if ps -p $SERVER_PID > /dev/null 2>&1; then
    osascript -e 'display notification "Server started at http://localhost:5001" with title "Demo Prep Tool" sound name "Glass"'
    open http://localhost:5001
else
    osascript -e 'display alert "Demo Prep Tool" message "Failed to start server. Check server.log for details." as critical'
    rm -f "$DIR/.server.pid"
    exit 1
fi
