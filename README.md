# Golf Distance Calculator

## Overview

Golf Distance Calculator is a web application project for my ICT239 Web Application Module, which is designed for golfers to log their swings, track distances, and visualize their performance. The application is built using Python with the Flask framework for the backend, MongoDB as the database, and various frontend technologies.

Note: You may find the documentation of my project in this repository.

## Project Structure

The project is structured into several components:

### 1. User Authentication and Registration

- **Files:** `user.py`, `auth.py`, `templates/auth/`
- **Description:** Manages user authentication and registration. The `User` class in `user.py` defines the user model.

### 2. Golf Set Management

- **File:** `golfSetData.py`
- **Description:** Handles golf set-related operations. The `GolfSet` class in `golfSetData.py` represents a golfer's set of golf clubs.

### 3. Swing Logging

- **File:** `swingData.py`
- **Description:** Manages golf swing data. The `Swing` class in `swingData.py` models a golf swing, including swing datetime, club used, swing speed, and estimated distance.

### 4. Upload Functionality

- **Files:** `app.py`, `upload.html`
- **Description:** Enables users to upload CSV or TXT files containing golf set or swing data. The backend processes the uploaded file, creating club or swing objects.

### 5. Swing Logging Page

- **Files:** `log2.html`, `log2.js`
- **Description:** Provides a page for users to log their golf swings. The `log2.js` script dynamically populates the club dropdown based on the selected golfer.

### 6. Swing Chart Visualization

- **Files:** `swingchart.html`, `swingchart.js`
- **Description:** Visualizes golf swing distances using Chart.js. The `swingchart.js` script fetches data from the server based on the selected golfer and updates the chart.

## How to Run

1. **Clone the repository**

2. **Install dependencies:**
bash
pip install -r requirements.txt

3. **Set up MongoDB:**
Ensure MongoDB is installed and running.
Update the MONGODB_SETTINGS configuration in config.py with your MongoDB connection details.

4. **Run the application:**
bash
python app.py
The application will be accessible at http://localhost:5000.
