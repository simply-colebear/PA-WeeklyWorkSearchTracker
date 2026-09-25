#!/bin/bash
# One-click weekly report generation
# # Usage: ./scripts/weekly_generate.sh [--last-week]
#
set -e
#
#
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
#
cd "$PROJECT_ROOT"
#
# Activate venv
if [[ -f ".venv/bin/activate" ]]; then
	source .venv/bin/activate
fi

# Determine week start date
if [[ "$1" == "--last-week" ]] || [[ "$1" == "-l" ]]; then
	WEEK_START=$(date -d "last monday" +%Y-%m-%d)
else
	WEEK_START=$(date +%Y-%m-%d)
fi

echo "=========================================="
echo "PA UC Work Search Report Generator"
echo "=========================================="
echo "Week Start: $WEEK_START"
echo ""
# Run generator
python src/generate_weekly_report.py \
	--week-start "$WEEK_START" \
	--db-path data/raw/job_tracker.db
echo ""
echo "=========================================="
echo "[+] Done! Check the outputs/ directory"
echo "[i] outputs/ directory more information scriptREADME.md"
echo "=========================================="
