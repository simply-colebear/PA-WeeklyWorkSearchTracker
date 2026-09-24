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
### Create their own venv
```bash
python -m venv .venv
```

### Activate
```bash
.venv\Scripts\Activate.ps1
```


### Install from shared requirements.txt
```bash
pip install -r requirements.txt
```
*pip-sync requirements.txt can also be used*

### Run migration
```bash
alembic upgrade head
```
