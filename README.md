<center><h1> Member Profiles</h1></center>

## Event Management System

# Description:
  
A web-based platform that allows users to create events with password protection and manage members with customizable roles. Users can join events using passwords, and organizers can assign specific roles to participants (organizer, speaker, graduate, etc.).

# Main Features

## Core Features:

### \- User Registration & Authentication

  \- User accounts with profile pictures  
  \- Secure login system

### \- Event Management

  \- Create events with titles, descriptions, and passwords  
  \- Set event types (graduation, conference, meeting, etc.)  
  \- Public/private event visibility options

### \- Member Management

  \- Join events using passwords  
  \- Customizable roles (organizer, speaker, graduate, student, etc.)  
  \- Role-based permissions system

### \- Media Handling

  \- Profile picture uploads

## Advanced Features:

\- Event search and filtering  
\- Member directory per event  
\- Role-based access control

# API Usage

This project will use Django REST Framework to build the API.  
Optional External APIs for future enhancement.

# Project Structure

## Django Apps Structure:
```
member\_profiles/  
├── users/                 \# User authentication & profiles  
│   ├── models.py         \# User model  
│   ├── serializers.py    \# User serializers  
│   ├── urls.py               \# Urls  
│   └── views.py           \# Authentication endpoints  
├── events/               \# Event management  
│   ├── models.py         \# Event model  
│   ├── serializers.py    \# Event serializers  
│   ├── urls.py               \# Urls  
│   └── views.py           \# Event endpoints  
├── members/              \# Event membership management  
│   ├── models.py         \# EventMember model  
│   ├── serializers.py    \# Member serializers  
│   ├── urls.py               \# Urls  
│   └── views.py           \# Membership endpoints  
└── media/               \# File upload handling  
    └── uploads/         \# User and event files
```

## Database Models:

\- User: username, email, password, profile\_picture, bio  
\- Event: title, description, event\_type, password, creator, event\_date  
\- EventMember: user, event, role

## **Relationships:**

- **User → Event** (One-to-Many): A user can create multiple events  
- **User → EventMember** (One-to-Many): A user can participate in multiple events  
- **Event → EventMember** (One-to-Many): An event can have multiple participants

### **ERD Diagram:**

*(Visual representation showing tables with fields and relationships)*

<div align="center">
  <img src="/static/images/erd visual representation.drawio (1).png" alt="ERD Diagram">
</div>

### **Field Specifications:**

#### **User Table:**

| Field | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | Integer | Primary Key, Auto-increment | Unique user identifier |
| username | String(100) | Unique, Not Null | User's display name |
| email | String(255) | Unique, Not Null | User's email address |
| password | String(100) | Not Null | Hashed password |
| profile\_picture | String(255) | Optional | Profile image path |
| bio | Text | Optional | User biography |

#### **Event Table:**

| Field | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | Integer | Primary Key, Auto-increment | Unique event identifier |
| title | String(200) | Not Null | Event title |
| description | Text | Not Null | Event description |
| event\_type | String(20) | Not Null | Type: graduation, conference, etc. |
| event\_password | String(100) | Not Null | Password for joining |
| creator\_id | Integer | Foreign Key (User.id) | Event creator |
| event\_date | DateTime | Not Null | Event date and time |
| created\_at | DateTime | Not Null | Event creation timestamp |

#### **EventMember Table:**

| Field | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | Integer | Primary Key, Auto-increment | Unique membership ID |
| user\_id | Integer | Foreign Key (User.id) | Member user |
| event\_id | Integer | Foreign Key (Event.id) | Associated event |
| role | String(20) | Default: 'participant' | Member's role in the event |
| bio | Text | Optional | Event-specific biography |
| specialization | String(100) | Optional | Member specialization |
| join\_date | DateTime | Not Null | Join timestamp |

### **Constraints:**

- **Unique Constraint:** `(user_id, event_id)` in EventMember table  
- **Foreign Key Constraints:** Proper cascade delete rules  
- **Indexes:** On frequently searched fields (username, email, event\_type)


---

## **API Endpoints**

### **Authentication Endpoints:**

| Method | Endpoint | Description | Request Body | Response |
| :---- | :---- | :---- | :---- | :---- |
| **POST** | `/api/auth/register/` | User registration | `{username, email, password}` | `{user_id, token}` |
| **POST** | `/api/auth/login/` | User login | `{email, password}` | `{user_id, token}` |
| **POST** | `/api/auth/logout/` | User logout | `{token}` | `{message: "Logged out"}` |
| **GET** | `/api/auth/profile/` | Get user profile | `{token}` | `{user_data}` |
| **PUT** | `/api/auth/profile/` | Update user profile | `{token, bio, profile_picture}` | `{updated_user}` |

### **Event Endpoints:**

| Method | Endpoint | Description | Request Body | Response |
| :---- | :---- | :---- | :---- | :---- |
| **GET** | `/api/events/` | List all public events | `{token}` | `[event_list]` |
| **POST** | `/api/events/create/` | Create a new event | `{token, title, description, event_type, event_password, event_date}` | `{event_id}` |
| **GET** | `/api/events/{event_id}/` | Get event details | `{token}` | `{event_details}` |
| **PUT** | `/api/events/{event_id}/` | Update event (creator only) | `{token, updated_fields}` | `{updated_event}` |
| **DELETE** | `/api/events/{event_id}/` | Delete event (creator only) | `{token}` | `{message: "Deleted"}` |
| **GET** | `/api/events/search/` | Search events | `{token, query, event_type}` | `[filtered_events]` |

### **Membership Endpoints:**

| Method | Endpoint | Description | Request Body | Response |
| :---- | :---- | :---- | :---- | :---- |
| **POST** | `/api/events/{event_id}/join/` | Join an event | `{token, event_password, display_name}` | `{membership_id}` |
| **GET** | `/api/events/{event_id}/members/` | List event members | `{token}` | `[member_list]` |
| **PUT** | `/api/members/{member_id}/role/` | Change member role (organizer only) | `{token, new_role}` | `{updated_member}` |
| **DELETE** | `/api/members/{member_id}/` | Remove member (organizer only) | `{token}` | `{message: "Removed"}` |
| **GET** | `/api/user/events/` | Get the user's events | `{token}` | `[user_events]` |

### **File Upload Endpoints:**

| Method | Endpoint | Description | Request Body | Response |
| :---- | :---- | :---- | :---- | :---- |
| **POST** | `/api/upload/profile-picture/` | Upload profile picture | `{token, image_file}` | `{image_url}` |

### **Authentication & Authorization Requirements:**

#### **Public Endpoints (No Auth Required):**

- `POST /api/auth/register/`  
- `POST /api/auth/login/`

#### **Protected Endpoints (Require Authentication):**

- All other endpoints require a valid JWT token

#### **Role-Based Permissions:**

- **Event Creator/Organizer:** Can update/delete event, manage members  
- **Event Members:** Can view event details and member list  
- **Non-Members:** Can only view public event information
---
### Developed by:
- **Haitham Elsherbeny** 

