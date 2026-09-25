#!/usr/bin/env python3
"""
PA UC Work Search Report Generator
Usage: python generate_weekly_report.py --week-start 2024-09-15 [--output report.pdf]
"""

import argparse
import sys
from pathlib import Path
from datetime import date, timedelta
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright, TimeoutError
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.models import Base, Job, Employer, UserConfig

def configure_database(db_path: str) -> tuple:
    """Initialize database connection"""
    engine = create_engine(f"sqlite:///{db_path}")
    Session = sessionmaker(bind=engine)
    return engine, Session

def get_weekly_applications(session, week_start: str) -> list:
    """Fetch applications for specified week"""
    start = date.fromisoformat(week_start)
    end = start + timedelta(days=6)
    
    stmt = select(Job).where(
        (Job.week_start == start) & (Job.status != 'withdrawn')
    ).order_by(Job.application_date)
    
    results = session.execute(stmt).scalars().all()
    
    # Enrich with employer data
    applications = []
    for job in results:
        applications.append({
            'date': job.application_date.isoformat(),
            'employer': job.employer.name,
            'contact_name': job.contact_name or '',
            'phone_email': job.contact_email or job.contact_phone or '',
            'how_applied': job.how_applied or 'Online',
            'results': job.results or ''
        })
    
    return applications

def render_html(applications: list, week_start: str, output_dir: Path) -> Path:
    """Render Jinja2 template to HTML"""
    env = Environment(
        loader=FileSystemLoader('templates/html'),
        autoescape=True
    )
    
    template = env.get_template('work_search_template.html')
    
    week_end = date.fromisoformat(week_start) + timedelta(days=6)
    html_content = template.render(
        applications=applications,
        week_start=week_start,
        week_end=week_end.isoformat(),
        generated_date=date.today().isoformat()
    )
    
    html_path = output_dir / f"work_search_{week_start}.html"
    html_path.write_text(html_content, encoding='utf-8')
    
    return html_path

def convert_to_pdf(html_path: Path, output_path: Path) -> Path:
    """Convert HTML to PDF using Playwright headless browser"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(f"file://{html_path.resolve()}")
            page.wait_for_load_state('networkidle')
            
            page.pdf(
                path=str(output_path),
                format='Letter',
                print_background=True,
                margin={'top': '0.75in', 'right': '0.75in', 'bottom': '0.75in', 'left': '0.75in'}
            )
        except TimeoutError:
            print("[X] Warning: Page took long to load, proceeding anyway")
        finally:
            browser.close()
    
    return output_path

def main():
    parser = argparse.ArgumentParser(
        description='Generate PA UC Work Search Report PDF'
    )
    parser.add_argument('--week-start', required=True,
                        help='Monday of the week (YYYY-MM-DD)')
    parser.add_argument('--output', default=None,
                        help='Output PDF path (default: auto-generated)')
    parser.add_argument('--db-path', default='data/raw/job_tracker.db',
                        help='Database file path')
    parser.add_argument('--clean-html', action='store_true',
                        help='Delete intermediate HTML after PDF generation')
    
    args = parser.parse_args()
    
    # Validate input
    try:
        week_start = date.fromisoformat(args.week_start)
    except ValueError:
        print("Error: Invalid date format. Use YYYY-MM-DD")
        sys.exit(1)
    
    # Setup paths
    base_dir = Path(__file__).parent.parent
    db_path = base_dir / args.db_path
    output_dir = base_dir / 'outputs'
    output_dir.mkdir(exist_ok=True)
    
    if args.output:
        pdf_output = base_dir / args.output
    else:
        pdf_output = output_dir / f"work_search_report_{args.week_start}.pdf"
    
    # Execute pipeline
    print(f"[i] Generating work search report for week starting {args.week_start}")
    
    engine, Session = configure_database(str(db_path))
    
    with Session() as session:
        applications = get_weekly_applications(session, args.week_start)
    
    print(f"   Found {len(applications)} applications for this week")
    
    if not applications:
        print("[i] No applications found. Creating empty report.")
    
    # Render HTML
    html_path = render_html(applications, args.week_start, base_dir / 'outputs')
    print(f"   [i]  Rendered HTML: {html_path}")
    
    # Convert to PDF
    convert_to_pdf(html_path, pdf_output)
    print(f"   [+] Generated PDF: {pdf_output}")
    
    # Cleanup if requested
    if args.clean_html and html_path.exists():
        html_path.unlink()
        print("   [i] Cleaned up temporary HTML")
    
    print(f"\n[+] Complete! Submit at: www.uc.pa.gov")

if __name__ == '__main__':
    main()