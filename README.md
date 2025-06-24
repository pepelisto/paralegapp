# ParalegApp – Automated Legal Case Tracking Platform

**ParalegApp** is a Django-powered web platform that automates daily monitoring of legal cases, helping attorneys track changes in court proceedings through smart alerts and collaborative tools.

In Chile (and many other countries), courts don't notify lawyers of case updates. ParalegApp scans court websites daily and alerts lawyers to new filings, rulings, or procedural changes.

## Features

- Secure user registration and login
- Add and manage legal cases for tracking
- Automatic daily web scraping of court portals
- Email notifications on case updates
- Dashboard with change history and timeline
- Case sharing and collaborative task assignment

## Tech Stack

- Python 3
- Django
- Requests / BeautifulSoup for web scraping
- PostgreSQL / SQLite
- SMTP for email delivery
- Bootstrap for frontend

## Why It Matters

Lawyers often miss important updates because there is no automated way to track changes on judicial websites. ParalegApp:

- Saves time by eliminating manual review  
- Prevents missed deadlines and filings  
- Improves collaboration within legal teams  

## Developer Notes

- Full-stack implementation: models, views, scraping, notifications, and templates
- Uses Django ORM and custom commands for background automation
- Designed for real-world legal workflows
- Smart notifications based on actual case changes

## Status

- Fully working MVP
- Not commercialized (lacked a business partner for go-to-market)
- Potential improvements: OAuth login, responsive design, broader court integration

