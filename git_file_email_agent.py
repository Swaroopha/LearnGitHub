#!/usr/bin/env python3
"""
Git File Email Agent
Extracts files changed today from git branch and sends email notification
"""

import subprocess
import smtplib
from datetime import datetime, date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import sys

class GitFileEmailAgent:
    def __init__(self, recipient_email, gmail_username, gmail_password):
        """
        Initialize the agent
        
        Args:
            recipient_email: Email to send the report to
            gmail_username: Gmail account username
            gmail_password: Gmail app password (not regular password)
        """
        self.recipient_email = recipient_email
        self.gmail_username = gmail_username
        self.gmail_password = gmail_password
        self.changed_files = []
        self.branch_name = None
        
    def get_current_branch(self):
        """Get the current git branch name"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True,
                text=True,
                check=True
            )
            self.branch_name = result.stdout.strip()
            return self.branch_name
        except subprocess.CalledProcessError as e:
            print(f"Error getting branch name: {e}")
            return None
    
    def get_files_changed_today(self):
        """Get all files changed today in the current branch"""
        try:
            today = date.today().isoformat()
            
            # Get commits from today
            result = subprocess.run(
                [
                    'git', 'log',
                    '--all',
                    f'--since={today}',
                    f'--until={date.today()}',
                    '--name-only',
                    '--pretty=format:%h|%an|%ai|%s'
                ],
                capture_output=True,
                text=True,
                check=True
            )
            
            if not result.stdout.strip():
                print("No commits found for today")
                return []
            
            lines = result.stdout.strip().split('\n')
            self.changed_files = []
            current_commit_info = None
            
            for line in lines:
                if '|' in line:  # This is a commit line
                    parts = line.split('|')
                    commit_hash = parts[0]
                    author = parts[1]
                    commit_date = parts[2][:10]  # Extract just the date
                    current_commit_info = {
                        'hash': commit_hash,
                        'date': commit_date,
                        'author': author
                    }
                elif line.strip() and current_commit_info:  # This is a filename
                    self.changed_files.append({
                        'filename': line.strip(),
                        'date': current_commit_info['date'],
                        'branch': self.branch_name or 'Unknown'
                    })
            
            return self.changed_files
        
        except subprocess.CalledProcessError as e:
            print(f"Error getting changed files: {e}")
            return []
    
    def create_html_table(self):
        """Create an HTML table from the changed files"""
        if not self.changed_files:
            return "<p>No files changed today.</p>"
        
        html = """
        <html>
        <head>
            <style>
                table {
                    border-collapse: collapse;
                    width: 100%;
                    margin: 20px 0;
                    font-family: Arial, sans-serif;
                }
                th {
                    background-color: #4CAF50;
                    color: white;
                    padding: 12px;
                    text-align: left;
                    border: 1px solid #ddd;
                }
                td {
                    padding: 10px;
                    border: 1px solid #ddd;
                }
                tr:nth-child(even) {
                    background-color: #f2f2f2;
                }
                tr:hover {
                    background-color: #ddd;
                }
            </style>
        </head>
        <body>
            <h2>Git Files Changed Today Report</h2>
            <table>
                <tr>
                    <th>Date</th>
                    <th>Filename</th>
                    <th>Branch</th>
                </tr>
        """
        
        for file_info in self.changed_files:
            html += f"""
                <tr>
                    <td>{file_info['date']}</td>
                    <td>{file_info['filename']}</td>
                    <td>{file_info['branch']}</td>
                </tr>
            """
        
        html += """
            </table>
            <p><small>Report generated on """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</small></p>
        </body>
        </html>
        """
        return html
    
    def send_email(self):
        """Send email with the file report"""
        if not self.changed_files:
            print("No files changed today. Email not sent.")
            return False
        
        try:
            # Create email message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Git Files Changed Today - {self.branch_name or 'Unknown Branch'}"
            msg['From'] = self.gmail_username
            msg['To'] = self.recipient_email
            
            # Create HTML content
            html_content = self.create_html_table()
            
            # Attach HTML part
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email via Gmail SMTP
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.gmail_username, self.gmail_password)
            server.sendmail(self.gmail_username, self.recipient_email, msg.as_string())
            server.quit()
            
            print(f"✓ Email sent successfully to {self.recipient_email}")
            return True
        
        except smtplib.SMTPAuthenticationError:
            print("✗ Error: Gmail authentication failed.")
            print("  Make sure you're using an App Password, not your regular Gmail password.")
            print("  Generate one at: https://myaccount.google.com/apppasswords")
            return False
        except Exception as e:
            print(f"✗ Error sending email: {e}")
            return False
    
    def run(self):
        """Execute the agent"""
        print("=" * 60)
        print("Git File Email Agent")
        print("=" * 60)
        
        # Get current branch
        print("\n1. Fetching current branch...")
        if not self.get_current_branch():
            print("✗ Failed to get branch name")
            return False
        print(f"   ✓ Current branch: {self.branch_name}")
        
        # Get files changed today
        print("\n2. Fetching files changed today...")
        self.get_files_changed_today()
        print(f"   ✓ Found {len(self.changed_files)} file(s) changed today")
        
        if self.changed_files:
            print("\n3. Files found:")
            for file_info in self.changed_files:
                print(f"   - {file_info['filename']} ({file_info['date']})")
        
        # Send email
        print("\n4. Sending email...")
        success = self.send_email()
        
        print("\n" + "=" * 60)
        return success


def main():
    """Main entry point"""
    # Configuration
    RECIPIENT_EMAIL = "swarooj@gmail.com"
    GMAIL_USERNAME = input("Enter your Gmail address: ").strip()
    GMAIL_PASSWORD = input("Enter your Gmail app password: ").strip()
    
    # Create and run agent
    agent = GitFileEmailAgent(RECIPIENT_EMAIL, GMAIL_USERNAME, GMAIL_PASSWORD)
    success = agent.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
