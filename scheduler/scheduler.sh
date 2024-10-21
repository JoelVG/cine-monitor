#!/usr/bin/env bash

# script to setup cron job to run the cine monitor python script everyday at 10AM

# Exit immediately if a command exits with a non-zero status
set -e

# Get parent path of current directory
parent_dir=$(dirname "$(dirname "$(readlink -f "$0")")")

# Get python path
python_dir=$(which python)

# Ensure the log file exists and is writable
touch $parent_dir/monitor.log
chmod 644 $parent_dir/monitor.log || { echo "Failed to set permissions on log file"; exit 1; }
chmod +x $parent_dir/monitor.py || { echo "Failed to set permissions on python script"; exit 1; }

# Create a new crontab entry
cron_job="0 10 * * * $python_dir $parent_dir/monitor.py >> $parent_dir/monitor.log 2>&1"

if ! (crontab -l 2>/dev/null || true; echo "$cron_job") | crontab -; then
    echo "Failed to set up cron job"
    exit 1
fi

echo "Cron job set up to run everyday at 10AM"
