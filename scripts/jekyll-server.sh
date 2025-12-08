#!/bin/bash

# Jekyll Server Management Script
# This script manages Jekyll server startup and shutdown to avoid port conflicts

JEKYLL_PID_FILE="../.jekyll.pid"
JEKYLL_PORT=4000

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if port is in use
check_port() {
    if lsof -Pi :$JEKYLL_PORT -sTCP:LISTEN -t >/dev/null ; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to kill existing Jekyll processes
kill_existing_processes() {
    log_info "Checking for existing Jekyll processes..."

    # Find and kill all Jekyll processes
    JEKYLL_PIDS=$(ps aux | grep -E "bundle exec jekyll|jekyll serve|jekyll s" | grep -v grep | awk '{print $2}')

    if [ ! -z "$JEKYLL_PIDS" ]; then
        log_warn "Found existing Jekyll processes, terminating..."
        echo "$JEKYLL_PIDS" | xargs kill -9 2>/dev/null
        sleep 2
        log_info "Existing processes terminated."
    else
        log_info "No existing Jekyll processes found."
    fi
}

# Function to start Jekyll server
start_server() {
    log_info "Starting Jekyll server on port $JEKYLL_PORT..."

    # Remove old PID file if exists
    [ -f "$JEKYLL_PID_FILE" ] && rm -f "$JEKYLL_PID_FILE"

    # Clean up Sass cache before starting
    [ -d "../.sass-cache" ] && rm -rf ../.sass-cache

    # Start Jekyll server in background (disable watch to avoid symlink issues)
    ./scripts/run-jekyll.sh serve --host 0.0.0.0 --port $JEKYLL_PORT --no-watch &
    JEKYLL_PID=$!

    # Save PID
    echo $JEKYLL_PID > "$JEKYLL_PID_FILE"
    log_info "Jekyll server started with PID: $JEKYLL_PID"

    # Wait a bit and check if server is running
    sleep 3
    if kill -0 $JEKYLL_PID 2>/dev/null; then
        log_info "Jekyll server is running successfully!"
        log_info "Visit: http://localhost:$JEKYLL_PORT"
    else
        log_error "Failed to start Jekyll server."
        [ -f "$JEKYLL_PID_FILE" ] && rm -f "$JEKYLL_PID_FILE"
        exit 1
    fi
}

# Function to stop Jekyll server
stop_server() {
    if [ -f "$JEKYLL_PID_FILE" ]; then
        JEKYLL_PID=$(cat "$JEKYLL_PID_FILE")
        if kill -0 $JEKYLL_PID 2>/dev/null; then
            log_info "Stopping Jekyll server (PID: $JEKYLL_PID)..."
            kill $JEKYLL_PID
            sleep 2
            if kill -0 $JEKYLL_PID 2>/dev/null; then
                log_warn "Force killing Jekyll server..."
                kill -9 $JEKYLL_PID
            fi
        else
            log_warn "Jekyll server process not found."
        fi
        rm -f "$JEKYLL_PID_FILE"
        log_info "Jekyll server stopped."
    else
        log_info "No Jekyll server PID file found."
    fi
}

# Function to show status
show_status() {
    if [ -f "$JEKYLL_PID_FILE" ]; then
        JEKYLL_PID=$(cat "$JEKYLL_PID_FILE")
        if kill -0 $JEKYLL_PID 2>/dev/null; then
            log_info "Jekyll server is running (PID: $JEKYLL_PID)"
            log_info "Port: $JEKYLL_PORT"
            log_info "URL: http://localhost:$JEKYLL_PORT"
        else
            log_warn "Jekyll server PID file exists but process is not running."
            rm -f "$JEKYLL_PID_FILE"
        fi
    else
        log_info "Jekyll server is not running."
    fi
}

# Function to show help
show_help() {
    echo "Jekyll Server Management Script"
    echo "================================"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start   - Start Jekyll server (default if no command specified)"
    echo "            Automatically handles port conflicts and process cleanup"
    echo ""
    echo "  stop    - Stop running Jekyll server"
    echo "            Safely terminates the server process"
    echo ""
    echo "  restart - Restart Jekyll server"
    echo "            Stops current server, cleans up processes, then starts new server"
    echo ""
    echo "  status  - Show current server status"
    echo "            Displays PID, port, and URL if server is running"
    echo ""
    echo "Examples:"
    echo "  $0              # Start server (default)"
    echo "  $0 start        # Start server explicitly"
    echo "  $0 stop         # Stop server"
    echo "  $0 restart      # Restart server"
    echo "  $0 status       # Check server status"
    echo ""
    echo "The script automatically:"
    echo "  - Detects and terminates conflicting processes"
    echo "  - Uses port 4000 (configured in _config.yml)"
    echo "  - Disables file watching to avoid symlink issues"
    echo "  - Provides colored status output"
}

# Main script logic
COMMAND="${1:-}"

case "$COMMAND" in
    start|"")
        log_info "Starting Jekyll server..."
        kill_existing_processes
        start_server
        ;;
    stop)
        stop_server
        ;;
    restart)
        log_info "Restarting Jekyll server..."
        stop_server
        sleep 1
        kill_existing_processes
        start_server
        ;;
    status)
        show_status
        ;;
    help|-h|--help)
        show_help
        ;;
    *)
        log_error "Unknown command: $COMMAND"
        echo ""
        show_help
        exit 1
        ;;
esac
