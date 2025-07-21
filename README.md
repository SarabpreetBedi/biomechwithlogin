# Pitcher Biomechanics Tracker

This project is a web application for tracking and analyzing pitcher biomechanics sessions. It uses [Streamlit](https://streamlit.io/) for the UI and [Supabase](https://supabase.com/) for authentication, storage, and database management.

## Steps to Run the Application

### a) Using the "YouTube Link" Option
- When the **YouTube Link** radio button is selected in the upload form, you must provide a valid YouTube URL in the "YouTube Link" field. This is required for session upload when this option is checked.
- With **YouTube Link** selected, you can upload either a CSV file (for kinematic data) or a video file. Both are accepted.

### b) Using the "Upload Video File" Option
- When the **Upload Video File** radio button is selected, you must upload a video file (mp4, mov, avi, etc.).
- The YouTube Link field is automatically disabled and its value will not be stored in the Supabase table.

### c) Session Variable Issues
- If you encounter issues with session variables (e.g., uploads not working or UI not updating), try logging out and logging back in before uploading CSV or video files again.
- The application is designed to handle file uploads smoothly, including setting a time interval for uploading video or CSV files to the Supabase database.

### d) Granting Admin Access
- To grant someone admin privileges, add their email address to the `ADMIN_EMAILS` list in your `.streamlit/secrets.toml` file, for example:
  ```toml
  ADMIN_EMAILS = ["mmueller4@rogers.com", "anotheremail4@rogers.com"]
  ```
- If you are using Streamlit Cloud, make sure to update the secrets in your Streamlit Cloud app account as well.
- After adding a new admin email (e.g., `anotheremail4@rogers.com`), that user must create a profile by signing up through the SignUp UI before they are recognized as an admin.

---

## Table of Contents
- [Features](#features)
- [File Overview](#file-overview)
- [Setup Instructions](#setup-instructions)
- [How to Use the UI](#how-to-use-the-ui)
  - [User Workflow](#user-workflow)
  - [Admin Workflow](#admin-workflow)
  - [Correct Usage](#correct-usage)
  - [Incorrect Usage](#incorrect-usage)
- [Supabase Integration](#supabase-integration)
- [Troubleshooting](#troubleshooting)

---

## Features
- User authentication (login/signup)
- Admin and regular user roles
- Upload and manage player sessions (CSV/video)
- View, analyze, and compare sessions
- Admin tools for data management

## File Overview
- **`auth.py`**: Handles authentication, login, signup, and admin detection. Manages user sessions and profile state.
- **`your_main_app.py`**: Main application logic. Contains all UI tabs (upload, view, compare, admin tools), handles file uploads, session management, and data visualization.
- **`app.py`**: Entry point. Routes users to login/signup or the main app based on authentication state.

## Setup Instructions
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure Streamlit secrets:**
   - Create a `.streamlit/secrets.toml` file with your Supabase credentials:
     ```toml
     SUPABASE_URL = "<your-supabase-url>"
     SUPABASE_SERVICE_ROLE_KEY = "<your-supabase-service-role-key>"
     ADMIN_EMAILS = ["admin1@example.com", "admin2@example.com"]
     ```
     - `ADMIN_EMAILS` can be a list or a comma-separated string.
3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## How to Use the UI

### User Workflow
1. **Login or Sign Up:**
   - Use your email and password to log in or create a new account.
2. **Upload Session:**
   - Go to the "Upload Session" tab.
   - Enter player and session details.
   - Upload a CSV (kinematic data) or video file, or provide a YouTube link.
   - Click "Upload" to save the session to Supabase.
3. **View Sessions:**
   - Use the "View Sessions" tab to select a player and session.
   - Watch the video, view notes, and analyze kinematic data.
4. **Compare Sessions:**
   - Use the "Compare Sessions" tab to view two sessions side-by-side.
5. **Delete Sessions:**
   - In the "Admin" tab (or "User Tools" for regular users), delete your own sessions and associated files.

### Admin Workflow
- Admins have access to all users' data and can:
  - Delete any session or player
  - View the entire database
  - Remove players with no sessions
  - Use all user features

### Correct Usage
- Always log in with your own credentials.
- When uploading, fill in all required fields (player name, team, session name, date, and file/link).
- Only upload valid CSV or video files (mp4, mov, avi) or a correct YouTube link.
- Use the provided UI buttons for all actions (upload, delete, view, compare).
- Admins should use the "Admin" tab for global data management.

### Incorrect Usage
- Do **not** try to upload unsupported file types or leave required fields blank.
- Do **not** attempt to bypass the UI (e.g., by directly modifying the database or storage).
- Do **not** share your credentials or use another user's account.
- Do **not** attempt to delete or modify data you do not own (unless you are an admin).
- Do **not** refresh the browser during an upload or critical operation (may cause duplicate or incomplete data).

## Supabase Integration
- All user, player, and session data is stored in Supabase tables.
- Files (CSV, video) are uploaded to Supabase Storage.
- Only authenticated users can access their own data (except admins).
- Admins are determined by the `ADMIN_EMAILS` list in Streamlit secrets.

## Troubleshooting
- **Login/Signup issues:** Ensure your email is not already registered. Use the correct password.
- **Upload errors:** Check file type and size. Ensure all fields are filled.
- **Data not appearing:** Try logging out and back in, or refresh the page.
- **Permission errors:** Only admins can access all data. Regular users can only manage their own.

---

For further help, check the code in `auth.py`, `your_main_app.py`, and `app.py` or contact the project maintainer. 