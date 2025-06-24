ParalegApp – Automated Legal Case Tracking Platform
ParalegApp is a Django-powered web platform that automates daily monitoring of legal cases, helping attorneys track changes in court proceedings through smart alerts and collaborative tools.

Lawyers don’t always receive official updates when there’s a court change. ParalegApp ensures they never miss critical developments by scanning court websites daily and sending alerts for meaningful updates.

🚀 Core Functionality
User registration and authentication – lawyers can securely log in.

Case management – add cases to track and view status updates.

Automated web scraping – daily checks for changes in case records on court portals.

Smart email alerts – notifies users of new court decisions, filings, or status updates.

Dashboard with change history – view case timelines and update summaries in the app.

Collaboration between lawyers – share cases, assign tasks, and jointly manage workflows.

🧱 Project Structure
'''
graphql
Copiar
ParalegApp/
├── app/                      # Django models: users, cases, tasks, collaborations
├── templates/                # HTML templates for case dashboard and email notifications
├── webscrap/                # Daily scraper module for court websites
├── notifications/           # Email handling logic and alerts
├── static/                  # CSS, JS, static assets
├── settings/                # Django configuration
└── manage.py                # Django admin & custom commands
'''

🔧 Tech Stack
Python 3

Django (web, ORM, users)

Requests / BeautifulSoup (web scraping)

PostgreSQL / SQLite (persistent storage)

SMTP email delivery

Bootstrap (basic UI)

💡 Why It Matters
Lawyers in Chile (and many jurisdictions) have to manually review court websites daily to catch updates. ParalegApp allows them to:

Save time and stay compliant by automating monitoring

Never miss deadlines triggered by court filings

Collaborate efficiently with colleagues on shared cases

🧠 Your Role & Achievements
Full-stack development: designed models, views, templates, and scraping logic

Automation: built custom Django commands and scheduling for daily scraping

User-centric design: created intuitive dashboards for case tracking and updates

Email integration: automatic notifications for real-world users

⚠️ Project Status
🟢 Functionally complete – all core features are implemented

⚠️ Not yet commercialized due to lack of marketing and sales partnership

🔧 Potential improvements: OAuth login, mobile-friendly UI, and broader case-sharing features# paralegapp
