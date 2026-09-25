# Scripts Directory README.md

---
- OS: Windows 11
- Usage: powershell
- version: 002
- createdDate: 2026-09-24
- updatedDate: 2026-09-25
- tags: #configurationFile 
---

For file *scripts\weekly_generate.ps1* individual will need to set assignmentfor output path. At this time, this is going to be considered the local Downloads folder.

Create and activate python virtual environment: 
```bash"
python -m venv .venv
.venv\Scripts\Activate.ps1
```
Individual will need to set environment variable *$CUSTOM_OUTPUT_PATH*.
- This enables user to configure at custom output location; however, 
- User(s) local Download folder is the most common place user(s) would look for output. 

```bash
$CUSTOM_OUTPUT_PATH = "C:\Users\..\Downloads"
```
#note-simply-colebear
> In the future this custom configuration may be disable to create a more streamlined process. This file will then contain the updates to set custom output path if docker container or some ftp server is decided to be more suitable for end-user.


