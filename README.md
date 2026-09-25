# PA-WeeklyWorkSearchTracker
Utility used to automattically create .pdf file for PA unemployment benefit requirement. This utiliity can be use a job posting/ summary to create the neccessary .pdf file required for archival purposes related to PA Unemployment Benefits. 

## Summary:

> Initial ReadMe file for automatic weekly activity log for PA unemployment work search traking. 
>
> simply-colebear: 09/25/2026 - Upload of initial configuration for PA Weekly Work Search Tracker Utility. Included requirements.txt file to install dependencies for project)

## Initial Install Script:
```bash
git clone https://github.com/yourusername/pa-work-search-tracker.git
cd pa-work-search-tracker
```
### Create loca virtual python environment *.venv*
```bash
python -m venv .venv
```

### Install dependencies from requirements.txt (included in steps for *Quick Start Guide*)
```bash
pip install -r requirements.txt
# *"pip-sync requirements.txt" can also be used*
```

###
Once cloned and virtual environment configuration complete. Please Complete the following steps before *Quick Start Guide* can be successfully executed. 
    1. Read full ~/scripts/sciptsREADME.md for scripts configuration and setup settings. Since #alpha-v1 these options need configured manually to enable scalability, cross-collabortion, and local security. 
    2. Job Applications/ Summary of Jobs and URLs that have been completed for application submission. This will need uploaded either during the system through entry in CMD or through a .JSON import. 
    3. Add sample --employer information based off own applications
        ``` bash
        python src/api/add_application.py --employer "[SAMPLE_EMPLOYER]" --date [APPLICATION_DATE] --position "[POSITION_APPLIEDFOR]"
        ```

## Quick Start Guide:

The following bash script moves user to directory, install dependencies, maps database, and adds sample job applications
```bash
cd ~/projects/pa-work-search-tracker
pyhton source .venv/bin/activate
#.venv\Scripts\Activate.ps1 if above command gives error
pip install -r requirements.txt
playwright install chromium
# Run migration
alembic upgrade head

# Add an application
python src/api/add_application.py --employer "The Allen Thomas Insurance Group" --date 2026-04-22 --position "Software Engineer"

python src/api/add_application.py --employer "Parker Construction" --date 2026-04-23 --position "Software Engineer"

python src/api/add_application.py --employer "Walmart" --date 2026-09-18 --position "Senior Software Engineer"

python src/api/add_application.py --employer "Allstate Insurance" --date 2026-09-19 --position "Software Engineer (GuideWire)"

# Template for adding new applications. 
# python src/api/add_application.py --employer "[SAMPLE_EMPLOYER]" --date [APPLICATION_DATE] --position "[POSITION_APPLIEDFOR]"

```



#### Generate this week's reports
```powershell
.\scripts\weekly_generate.ps1
```

##### Generate this week's reports (Linux)
```bash
#./scripts/weekly_generate.sh
````

#### Generate last week's report (most common use case)
```powershell
.\scripts\weekly_generate.ps1 -LastWeek
````

##### Generate last week's report (Linux)
```bash
./scripts/weekly_generate.sh --last-week
````

#### View database contents
```bash
sqlite3 data/raw/job_tracker.db "SELECT * FROM jobs;"
````

## Known Issues
#knownIssues_PA-WorkSearchTracker

### alembic.ini Duplicate Error
If you see `DuplicateOptionError: {script_location, prepend_sys_path}`, edit `alembic.ini` and ensure the following:
    - `script_location = alembic` appears only once in the `[alembic]` section.
    - `prepend_sys_path = .` appears only once in the `[alembic]` section

### alembic.ini "bar:c"

 If you see `WinError 123` including some issue with a filename, directory name, or volume label is mentioned to be incorrect.
    \PA-WeeklyWorkSearchTracker\\bar:C
        - Remove or comment out the following lines in `[alembic]` section
        ``` .ini
        version_path_separator = os
        version_locations = %(here)s:%(here)s/alembic/versions
        ```




