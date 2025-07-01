# Pharmacy Management System Documentation

## Core Files and Their Purposes

### 1. reg.py (Login System)
- **Main Login Interface**: Handles user authentication and registration
- **Key Features**:
  - User/Admin login
  - New user registration with email verification
  - Password reset functionality
  - OTP verification system
  - Form validation
  - Animated UI elements

### 2. Admin.py (Admin Dashboard)
- **Admin Control Panel**: Manages users and system administration
- **Key Features**:
  - User management (CRUD operations)
  - Admin account management
  - Data table visualization
  - User data modification
  - Security validation
  - Admin privilege controls

### 3. pharmacy.py (Main Application)
- **Medicine Management System**: Handles pharmacy operations
- **Key Features**:
  - Medicine inventory management
  - Medicine information tracking
  - Smart AI assistant for queries
  - Search functionality
  - Data visualization
  - Stock management

### 4. create_admin.py (Database Setup)
- **Database Initialization**: Sets up required database tables
- **Key Features**:
  - Admin table creation
  - Database schema setup
  - Initial setup configuration

## Database Structure

### Tables
1. **login**
   - User credentials
   - Email verification
   - Account details

2. **admin_login**
   - Admin credentials
   - Admin privileges
   - Admin management

3. **pharmacy**
   - Medicine inventory
   - Medicine details
   - Stock information

## Security Features

1. **Password Security**
   - Bcrypt hashing
   - Encrypted storage
   - Secure validation

2. **Access Control**
   - Role-based access
   - Session management
   - Login verification

3. **Data Validation**
   - Input sanitization
   - Form validation
   - Error handling

## User Interface Components

1. **Animated Elements**
   - Button animations
   - Form transitions
   - Visual feedback

2. **Custom Widgets**
   - AnimatedButton
   - FadeLabel
   - AnimatedEntry

3. **Dialog Windows**
   - Error messages
   - Confirmation dialogs
   - Information popups

## Core Functionalities

### User Management
- Registration with email verification
- Password recovery system
- Profile management
- Access control

### Admin Functions
- User data management
- System monitoring
- Admin account creation
- Database management

### Pharmacy Operations
- Medicine inventory
- Stock tracking
- Medicine information
- AI-powered assistance

## Technologies Used

1. **Frontend**
   - Tkinter
   - Custom widgets
   - UI animations

2. **Backend**
   - MySQL database
   - Python core
   - Email integration

3. **Security**
   - Bcrypt encryption
   - OTP verification
   - Session management

## System Requirements

1. **Software Dependencies**
   - Python 3.x
   - MySQL Server
   - Required Python packages:
     - mysql-connector-python
     - bcrypt
     - pillow
     - smtplib

2. **Database Configuration**
   - Database name: mydata
   - Default admin credentials setup
   - Table structures

## File Structure