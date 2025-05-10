#!/bin/bash

# Check if log file is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <logfile>"
    exit 1
fi

LOG_FILE=$1

# 1. Request Counts
echo "=== Request Counts ==="
total_requests=$(wc -l < "$LOG_FILE")
echo "Total requests: $total_requests"

get_requests=$(grep -c 'GET' "$LOG_FILE")
echo "GET requests: $get_requests"

post_requests=$(grep -c 'POST' "$LOG_FILE")
echo "POST requests: $post_requests"

# 2. Unique IP Addresses
echo -e "\n=== Unique IP Analysis ==="
unique_ips=$(awk '{print $1}' "$LOG_FILE" | sort -u | wc -l)
echo "Total unique IPs: $unique_ips"

echo -e "\nRequests per IP (Top 10):"
awk '{print $1}' "$LOG_FILE" | sort | uniq -c | sort -nr | head -10

echo -e "\nGET/POST counts per IP (Top 10):"
awk '{print $1,$6}' "$LOG_FILE" | grep -E 'GET|POST' | sort | uniq -c | sort -nr | head -10

# 3. Failure Requests
echo -e "\n=== Failure Analysis ==="
failed_requests=$(awk '$9 ~ /^[45][0-9][0-9]$/ {print}' "$LOG_FILE" | wc -l)
failure_percentage=$(echo "scale=2; ($failed_requests/$total_requests)*100" | bc)
echo "Failed requests (4xx/5xx): $failed_requests ($failure_percentage%)"

# 4. Top User
echo -e "\n=== Most Active User ==="
awk '{print $1}' "$LOG_FILE" | sort | uniq -c | sort -nr | head -1

# 5. Daily Request Averages
echo -e "\n=== Daily Averages ==="
total_days=$(awk -F'[' '{print $2}' "$LOG_FILE" | awk '{print $1}' | cut -d: -f1 | sort -u | wc -l)
if [ "$total_days" -gt 0 ]; then
    avg_daily=$(echo "scale=2; $total_requests/$total_days" | bc)
    echo "Average requests per day: $avg_daily"
fi

# 6. Failure Analysis by Day
echo -e "\n=== Days with Highest Failures ==="
awk '$9 ~ /^[45][0-9][0-9]$/ {print $4}' "$LOG_FILE" | cut -d: -f1 | sort | uniq -c | sort -nr | head -5

# Additional Analyses
echo -e "\n=== Hourly Request Distribution ==="
awk -F'[ :]' '{print $5}' "$LOG_FILE" | sort | uniq -c | sort -k2 -n

echo -e "\n=== Status Code Breakdown ==="
awk '{print $9}' "$LOG_FILE" | sort | uniq -c | sort -nr

echo -e "\n=== Most Active User by Method ==="
echo "Top GET user:"
awk '$6 == "\"GET" {print $1}' "$LOG_FILE" | sort | uniq -c | sort -nr | head -1
echo "Top POST user:"
awk '$6 == "\"POST" {print $1}' "$LOG_FILE" | sort | uniq -c | sort -nr | head -1

echo -e "\n=== Failure Patterns by Hour ==="
awk '$9 ~ /^[45][0-9][0-9]$/ {print $4}' "$LOG_FILE" | cut -d: -f2 | sort | uniq -c | sort -nr | head -5

# Analysis Suggestions
echo -e "\n=== Suggestions ==="
echo "1. To reduce failures:"
echo "   - Investigate the most common error codes and their causes"
echo "   - Check the timing patterns of failures for server load issues"
echo "   - Review requests from IPs with high failure rates"

echo -e "\n2. Attention needed for:"
echo "   - Days/times with highest failure rates (shown above)"
echo "   - IPs making excessive requests (potential security concern)"

echo -e "\n3. Security considerations:"
echo "   - Review IPs with unusually high request volumes"
echo "   - Check for repeated failed requests from the same IPs"

echo -e "\n4. System improvement suggestions:"
echo "   - Scale resources during peak hours identified in hourly analysis"
echo "   - Implement rate limiting for abusive IPs"
echo "   - Optimize endpoints with high failure rates"