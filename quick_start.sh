#!/bin/bash

# GoPay with IntaSend - Quick Start Script
# This script helps you get started quickly with the IntaSend integration

set -e  # Exit on error

echo "============================================"
echo "  GoPay with IntaSend - Quick Start"
echo "============================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Check if .env exists
if [ -f ".env" ]; then
    print_warning ".env file already exists"
    read -p "Do you want to overwrite it? (y/n): " overwrite
    if [ "$overwrite" != "y" ]; then
        print_info "Using existing .env file"
    else
        cp env.intasend.example .env
        print_success "Created new .env file from template"
    fi
else
    cp env.intasend.example .env
    print_success "Created .env file from template"
fi

echo ""
print_info "Please update the .env file with your credentials:"
echo "  1. SUPABASE_URL and SUPABASE_ANON_KEY"
echo "  2. INTASEND_API_KEY and INTASEND_PUBLISHABLE_KEY"
echo "  3. Set INTASEND_TEST_MODE=true for sandbox testing"
echo ""

read -p "Press Enter once you've updated the .env file..."

# Load environment variables
source .env

# Verify environment variables are set
echo ""
print_info "Verifying environment variables..."

if [ -z "$SUPABASE_URL" ] || [ "$SUPABASE_URL" == "https://your-project.supabase.co" ]; then
    print_error "SUPABASE_URL not configured"
    exit 1
fi
print_success "SUPABASE_URL configured"

if [ -z "$SUPABASE_ANON_KEY" ] || [ "$SUPABASE_ANON_KEY" == "your-supabase-anon-key-here" ]; then
    print_error "SUPABASE_ANON_KEY not configured"
    exit 1
fi
print_success "SUPABASE_ANON_KEY configured"

if [ -z "$INTASEND_API_KEY" ] || [ "$INTASEND_API_KEY" == "your-intasend-secret-api-key-here" ]; then
    print_error "INTASEND_API_KEY not configured"
    exit 1
fi
print_success "INTASEND_API_KEY configured"

if [ -z "$INTASEND_PUBLISHABLE_KEY" ] || [[ ! "$INTASEND_PUBLISHABLE_KEY" == ISPubKey_* ]]; then
    print_error "INTASEND_PUBLISHABLE_KEY not configured"
    exit 1
fi
print_success "INTASEND_PUBLISHABLE_KEY configured"

# Check if Python is installed
echo ""
print_info "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    exit 1
fi
print_success "Python 3 is installed"

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    print_error "pip is not installed"
    exit 1
fi
print_success "pip is installed"

# Install dependencies
echo ""
print_info "Installing dependencies..."
pip install -r requirements.txt
print_success "Dependencies installed"

# Ask about database migration
echo ""
print_warning "Database Migration Required"
echo "You need to run the database migration in Supabase SQL Editor"
echo "File: database/intasend_migration.sql"
echo ""
read -p "Have you already run the database migration? (y/n): " migration_done

if [ "$migration_done" != "y" ]; then
    print_warning "Please run the database migration before starting the application:"
    echo "  1. Open Supabase SQL Editor"
    echo "  2. Copy contents of database/intasend_migration.sql"
    echo "  3. Execute the script"
    echo "  4. Verify tables created"
    echo ""
    read -p "Press Enter once migration is complete..."
fi

# Check which main file to use
echo ""
print_info "Checking application files..."

if [ -f "app/main_intasend.py" ]; then
    MAIN_FILE="app.main_intasend:app"
    print_success "IntaSend-enabled application found"
else
    MAIN_FILE="app.main:app"
    print_warning "Using standard application (no IntaSend)"
fi

# Start the application
echo ""
print_success "Setup complete! Starting application..."
echo ""
print_info "Application will be available at: http://localhost:8000"
print_info "API Documentation: http://localhost:8000/docs"
print_info "Press Ctrl+C to stop the server"
echo ""

# Wait a moment before starting
sleep 2

# Start uvicorn
uvicorn $MAIN_FILE --reload --host 0.0.0.0 --port 8000

