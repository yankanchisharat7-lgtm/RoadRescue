# 🚗 RoadRescue – On-Demand Roadside Assistance Platform

## 📌 Overview

**RoadRescue** is a Django-based web application designed to connect customers with nearby mechanics when they need roadside assistance.

The platform allows customers to find mechanics, view their details and services, book assistance, track booking status, receive notifications, and submit reviews.

Mechanics have a separate dashboard where they can manage their profile, availability, view customer bookings, and update service status.

The system provides separate workflows for **Customers, Mechanics, and Administrators**.

---

## 🎯 Problem Statement

Vehicle breakdowns can happen unexpectedly, and finding a reliable mechanic quickly can be difficult.

RoadRescue solves this problem by providing a centralized platform where users can:

* Find available mechanics
* Search mechanics based on location and vehicle type
* View mechanic information and ratings
* Request roadside assistance
* Track service progress
* Receive booking notifications
* Review completed services

Mechanics can use the platform to manage incoming service requests and update their availability and booking status.

---

## ✨ Key Features

### 👤 Customer Features

* Customer registration and login
* Separate customer dashboard
* Search and filter mechanics
* Search by:

  * Shop name
  * Location
  * Vehicle type
  * Rating
  * Availability
* View mechanic profiles
* View mechanic services and charges
* Book roadside assistance
* View booking details
* Track booking status
* Receive notifications
* View booking history
* Submit reviews after completed services
* Customer-specific logout functionality

---

### 🔧 Mechanic Features

* Separate mechanic registration and login
* Dedicated mechanic dashboard
* Mechanic profile management
* Upload mechanic/shop photo
* Manage shop information
* Manage service charges
* Set mechanic availability
* View incoming bookings
* Manage booking requests
* Update booking status

### Booking Status Flow

```text
Pending
   ↓
Accepted
   ↓
On The Way
   ↓
Completed
```

Mechanics can update the booking status, and customers are notified about the changes.

---

### 🔔 Notification System

RoadRescue provides notifications when the status of a booking changes.

For example:

```text
Pending → Accepted
Accepted → On The Way
On The Way → Completed
```

Customers can view these updates from their account.

---

### ⭐ Review System

Customers can provide reviews for mechanics after completing a service.

Reviews help future customers understand the quality and reliability of available mechanics.

---

### 👨‍💼 Admin Features

Django's built-in administration system can be used to manage the application's data and backend operations.

The administrator can manage application records such as:

* Users
* Mechanics
* Bookings
* Reviews
* Notifications

---

## 🛠️ Technology Stack

### Frontend

* HTML5
* CSS3
* Bootstrap
* JavaScript

### Backend

* Python
* Django

### Database

* SQLite

### Additional Technologies

* Django Authentication
* Django Forms
* Django ORM
* Django Email System
* Pillow
* Geopy

### Development Tools

* Visual Studio Code
* Git
* GitHub

---

## 🏗️ Project Structure

```text
RoadRescue/
│
├── accounts/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── bookings/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── core/
│   ├── urls.py
│   └── views.py
│
├── mechanics/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── notifications/
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── reviews/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── roadrescue/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│
├── media/
│
├── manage.py
├── requirements.txt
└── .gitignore
```

---

## 🔄 Application Workflow

### Customer Workflow

```text
Register
   ↓
Customer Dashboard
   ↓
Search Mechanics
   ↓
View Mechanic Details
   ↓
Book Mechanic
   ↓
Booking Created
   ↓
Wait for Mechanic
   ↓
Accepted
   ↓
Mechanic On The Way
   ↓
Service Completed
   ↓
Submit Review
```

### Mechanic Workflow

```text
Register as Mechanic
   ↓
Mechanic Dashboard
   ↓
Manage Profile
   ↓
Set Availability
   ↓
Receive Booking
   ↓
Accept Booking
   ↓
On The Way
   ↓
Complete Service
```

---

## 🔐 Authentication & Security

RoadRescue uses Django's authentication system to manage user accounts.

The application provides separate access flows for:

* Customers
* Mechanics

A mechanic account cannot be used to access the customer dashboard, and customer accounts cannot access the mechanic dashboard.

The project also uses Django's CSRF protection for POST forms and authentication decorators for protected pages.

---

## 📦 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/yankanchisharat7-lgtm/RoadRescue.git
```

### 2. Open the project

```bash
cd RoadRescue
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Start the development server

```bash
python manage.py runserver
```

### 8. Open the application

```text
http://127.0.0.1:8000/
```

---

## 📋 Requirements

The required Python packages are available in:

```text
requirements.txt
```

The project currently uses Django 6.0.6.

---

## 🧪 Testing

The application has been tested across the major workflows, including:

* Customer registration
* Mechanic registration
* Customer login
* Mechanic login
* Customer dashboard
* Mechanic dashboard
* Mechanic search
* Mechanic details
* Booking creation
* Booking status updates
* Notifications
* Reviews
* Mechanic profile management
* Mechanic availability
* Logout
* Authentication separation

The main application flow has been verified to work correctly.

---

## 👥 User Roles

| Role     | Main Responsibilities                                              |
| -------- | ------------------------------------------------------------------ |
| Customer | Find mechanics, create bookings, track services and submit reviews |
| Mechanic | Manage profile, availability, bookings and service status          |
| Admin    | Manage application data through Django Admin                       |

---

## 🚀 Future Improvements

Possible future enhancements include:

* Real-time mechanic location tracking
* Google Maps integration
* Online payment gateway
* SMS notifications
* Real-time chat between customers and mechanics
* Advanced mechanic recommendation system
* Emergency SOS functionality
* Mobile application
* Improved analytics and reporting
* Cloud deployment

---

## 📸 Project Highlights

RoadRescue provides a professional interface for:

* Customer dashboard
* Mechanic dashboard
* Mechanic search
* Mechanic profiles
* Booking management
* Notifications
* Reviews
* Authentication

---

## 🎓 Project Purpose

RoadRescue was developed as a web-based project to demonstrate the practical implementation of:

* Full-stack web development
* Django framework
* Database management
* User authentication
* Role-based workflows
* CRUD operations
* Form handling
* Booking management
* Notification systems
* Git and GitHub version control

---

## 👨‍💻 Development

**Project:** RoadRescue
**Type:** Web Application
**Framework:** Django
**Language:** Python
**Database:** SQLite
**Version Control:** Git & GitHub

---

## 📄 License

This project is developed for educational and project demonstration purposes.
