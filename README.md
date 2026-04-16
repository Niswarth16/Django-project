# College Management System

A comprehensive Django-based training institute management system similar to Hartron student portal with role-based access control for Students, Colleges/Institutes, and Administrators.

## Features

### User Roles & Authentication
- **Three User Types**: Student, College/Institute, Admin
- **Role-based Login**: Separate login pages for each user type
- **Secure Authentication**: Django authentication system with approval workflow
- **Profile Management**: Complete profile management for each user type

### Student Module
- Student registration with detailed profile
- View personal information and enrollment details
- Browse and enroll in courses
- View academic results and certificates
- Track course progress

### College Module
- Manage student records and profiles
- Upload and manage student data
- View student lists with search/filter functionality
- Manage course offerings
- Institute profile management

### Admin Module
- Comprehensive dashboard with system statistics
- Approve/reject student and college registrations
- View and manage all users
- Generate reports and analytics
- Full system control

### Technical Features
- **Responsive Design**: Bootstrap-based UI for all devices
- **Modern UI**: Clean, professional interface
- **Database**: SQLite (default) with proper models
- **Security**: Role-based access control and data validation
- **Search & Filter**: Advanced search for students and courses

## Project Structure

```
collegemanagement/
├── accounts/          # User authentication and roles
├── students/          # Student-specific functionality
├── colleges/          # College/institute management
├── courses/           # Course management and enrollment
├── core/              # Core functionality and dashboards
├── templates/         # HTML templates
├── static/            # Static files (CSS, JS, images)
└── media/             # User uploaded files
```

## Database Models

### User System
- **User**: Extended Django User with role and approval fields
- **StudentProfile**: Detailed student information
- **CollegeProfile**: Institute/college details

### Academic Models
- **Course**: Course information with duration and fees
- **Enrollment**: Student-course relationship with status tracking
- **Result**: Academic results and grades
- **Certificate**: Certificate management

## Installation & Setup

### Prerequisites
- Python 3.8+
- Django 5.2+
- pip package manager

### Installation Steps

1. **Clone or Download the Project**
   ```bash
   cd collegemanagement
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install django
   ```

4. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   # Follow prompts to create admin account
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   - Home Page: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - Login Page: http://127.0.0.1:8000/accounts/login/

## Default Admin Account
For testing purposes, a default admin account is created:
- **Username**: admin
- **Password**: admin123
- **Email**: admin@example.com

## User Registration & Approval Process

1. **Student Registration**
   - Visit `/accounts/signup/`
   - Select "Student" as user type
   - Fill registration form
   - Wait for admin approval
   - Complete student profile after approval

2. **College Registration**
   - Visit `/accounts/signup/`
   - Select "College/Institute" as user type
   - Fill institute details
   - Wait for admin approval
   - Setup college profile after approval

3. **Admin Access**
   - Use superuser account or create admin user
   - Access admin panel for user management
   - Approve pending registrations
   - Manage system settings

## Key Features Usage

### Student Dashboard
- View enrolled courses and progress
- Access results and certificates
- Update personal profile
- Browse available courses

### College Dashboard
- Manage student records
- Add/edit student information
- View enrollment statistics
- Manage course offerings

### Admin Dashboard
- System overview with statistics
- User approval workflow
- Generate reports
- Full administrative control

## Customization

### Adding New Fields
1. Update models in respective apps
2. Create and run migrations
3. Update forms and templates
4. Test functionality

### Custom Styling
- Modify templates in `/templates/` directory
- Add custom CSS in `/static/` directory
- Bootstrap 5.1.3 is used as the base framework

### Database Configuration
- Default: SQLite (development)
- Production: Configure PostgreSQL/MySQL in settings.py
- Update DATABASES setting accordingly

## Security Considerations

- All user inputs are validated
- CSRF protection enabled
- Role-based access control
- Password validation
- File upload restrictions

## Deployment

### Production Settings
1. Set `DEBUG = False`
2. Configure `ALLOWED_HOSTS`
3. Set up production database
4. Configure static files serving
5. Set up SSL/TLS
6. Use production WSGI server (Gunicorn/uWSGI)

### Environment Variables
For production, consider using environment variables for:
- `SECRET_KEY`
- Database credentials
- Email settings
- File storage paths

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## Support

For issues and questions:
1. Check documentation
2. Review error logs
3. Test with sample data
4. Contact development team

## License

This project is for educational purposes. Feel free to modify and use according to your requirements.

## Future Enhancements

- Email notifications
- Advanced reporting
- Mobile app integration
- Payment gateway integration
- Advanced analytics
- Multi-language support
- API endpoints for mobile apps

---

**Note**: This is a comprehensive training institute management system designed for educational institutions. The system provides role-based access control and modern web interface for efficient administration and student management.
