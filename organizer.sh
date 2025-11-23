#!/usr/bin/env bash
# organizer.sh
# Archives all CSV files with timestamps and recording detailed logs.

set -euo pipefail

ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"

# Ensures that archive directory exists
mkdir -p "$ARCHIVE_DIR"

# Generate timestamp in format: YYYYMMDD-HHMMSS
timestamp() { date +"%Y%m%d-%H%M%S"; }

# Collect all CSV files in the current directory
shopt -s nullglob
CSV_FILES=( *.csv )
shopt -u nullglob

# Exit if no CSV files are found
if [ ${#CSV_FILES[@]} -eq 0 ]; then
  echo "No CSV files found. Nothing to archive."
  exit 0
fi

# Process each CSV file
for file in "${CSV_FILES[@]}"; do
  ts=$(timestamp)
  base="${file%.csv}"
  newname="${base}-${ts}.csv"

  # If a file with the same name exists, add a random suffix
  if [ -e "$ARCHIVE_DIR/$newname" ]; then
    rand=$(printf "%04d" $((RANDOM % 10000)))
    newname="${base}-${ts}-${rand}.csv"
  fi

  # To write archive details and file content into the log file
  {
    echo "=== Archive Log Entry ==="
    echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "Original File: $file"
    echo "Archived As:   $ARCHIVE_DIR/$newname"
    echo "--- File Content ---"
    cat "$file"
    echo "--- End of Content ---"
    echo ""
  } >> "$LOG_FILE"

  # Move the file to the archive directory with the new name
  mv -- "$file" "$ARCHIVE_DIR/$newname"
  echo "Archived: $file -> $ARCHIVE_DIR/$newname"
done

# Final status message
echo "All CSV files archived."

