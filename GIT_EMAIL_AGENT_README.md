# Git File Email Agent

An automated Python agent that extracts files changed today from your git repository and sends an email notification with a formatted table report.

## Features

- ✓ Extracts all files changed today from your current git branch
- ✓ Displays results in a clean HTML table format with Date, Filename, and Branch name
- ✓ Sends email to swarooj@gmail.com automatically
- ✓ Manual trigger - run whenever you need
- ✓ Works with GitHub or any git repository

## Prerequisites

- Python 3.6+
- Git installed and configured
- A Gmail account (for sending emails)

## Setup Instructions

### Step 1: Generate Gmail App Password

Since Google disabled direct password login, you need to create an **App Password**:

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** if not already enabled
3. Go to [App Passwords](https://myaccount.google.com/apppasswords)
4. Select "Mail" and "Windows Computer"
5. Google will generate a 16-character password - **save this**

### Step 2: Run the Agent

Open PowerShell in the LearnGitHub directory and run:

```powershell
python git_file_email_agent.py
```

### Step 3: Provide Credentials

When prompted:
- **Gmail address**: Enter your Gmail address (the one with the app password)
- **App Password**: Enter the 16-character password from Step 1

## What It Does

1. **Connects to Git**: Fetches the current branch name
2. **Scans for Changes**: Identifies all files changed today (24-hour window)
3. **Creates Report**: Generates a formatted HTML table with:
   - Date (when the file was committed)
   - Filename (path of the changed file)
   - Branch name (current git branch)
4. **Sends Email**: Delivers the report to swarooj@gmail.com in a styled email

## Output Example

| Date       | Filename           | Branch  |
|------------|--------------------|---------|
| 2025-12-24 | src/main.py        | main    |
| 2025-12-24 | README.md          | main    |
| 2025-12-24 | config/settings.yml| main    |

## Usage Examples

### Basic Usage
```powershell
python git_file_email_agent.py
```

### Scheduling (Optional)

**Windows Task Scheduler**:
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger and action to run: `python C:\path\to\git_file_email_agent.py`

## Troubleshooting

### "Gmail authentication failed"
- Ensure you're using an **App Password**, not your regular Gmail password
- Double-check the 16-character password has no typos

### "No commits found for today"
- Your repository has no commits in the last 24 hours
- The agent only reports changes from the current calendar date

### "Error getting branch name"
- Make sure you're running the script from within a git repository
- Verify git is installed: `git --version`

## Files

- `git_file_email_agent.py` - Main agent script

## License

Open source - feel free to modify and use as needed.
