# Arabity Wain - Car Reporting System

## Overview

Arabity Wain is a Flask-based web application designed to help track lost and found vehicles in the Arab world. The system allows users to report lost cars and sightings, automatically matches reports based on license plates or chassis numbers, and facilitates communication through a mediator for privacy and security.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM with SQLite as default (configurable via DATABASE_URL)
- **Session Management**: Flask sessions with configurable secret key
- **File Uploads**: Local storage in static/uploads directory
- **Proxy Support**: ProxyFix middleware for deployment behind reverse proxies

### Frontend Architecture
- **Template Engine**: Jinja2 with Flask
- **Language Support**: Arabic (RTL layout)
- **Styling**: Custom CSS with CSS variables for theming
- **Responsive Design**: Mobile-friendly interface

### Authentication
- **Admin Access**: Simple password-based authentication for mediator dashboard
- **Session-based**: Uses Flask sessions to maintain admin login state
- **No User Registration**: Public reporting without user accounts

## Key Components

### Models (models.py)
1. **Report Model**
   - Stores both lost car reports and sighting reports
   - Fields: report_type, car_name, model, color, chassis, plate, location, phone, image_path
   - Indexed on chassis and plate for efficient matching
   - Soft deletion with is_active flag

2. **Match Model**
   - Records automatic matches between lost and sighting reports
   - Tracks matching rule (plate or chassis)
   - Foreign key relationships to both reports

### Core Utilities (utils.py)
1. **Normalization Functions**
   - normalize_plate(): Standardizes license plate format
   - normalize_chassis(): Standardizes chassis number format
   - Removes spaces, dashes, and special characters for consistent matching

2. **File Handling**
   - save_image(): Handles image uploads with unique naming
   - allowed_file(): Validates file extensions (PNG, JPG, JPEG, WEBP)
   - 5MB file size limit

3. **Matching Algorithm**
   - find_matches_for(): Automatically finds matching reports
   - Compares normalized plate and chassis numbers
   - Creates Match records for discovered connections

### Routes (routes.py)
1. **Public Routes**
   - Home page with system overview
   - Report creation (lost/sighting)
   - Search functionality
   - Contact page with mediator information

2. **Admin Routes**
   - Admin login/logout
   - Dashboard with recent matches
   - Report management interface

## Data Flow

1. **Report Creation**
   - User submits report (lost or sighting)
   - System normalizes plate/chassis data
   - Image uploaded and stored locally
   - Automatic matching triggered against existing reports

2. **Matching Process**
   - New reports compared against opposite type (lost vs sighting)
   - Matches created based on normalized plate or chassis numbers
   - Admin notified through dashboard

3. **Search Process**
   - Public search by plate or chassis
   - Returns status: clear, raised (lost report exists), or matched
   - For matches, displays basic car information without contact details

4. **Admin Workflow**
   - Admin reviews matches in dashboard
   - Contact information available for both parties
   - Facilitates communication between reporter and spotter

## External Dependencies

### Python Packages
- Flask: Web framework
- Flask-SQLAlchemy: ORM integration
- Werkzeug: WSGI utilities and security
- python-dotenv: Environment variable management

### Environment Variables
- `DATABASE_URL`: Database connection string
- `SESSION_SECRET`: Flask session encryption key
- `ADMIN_PASSWORD`: Mediator dashboard access
- `OWNER_PHONE`: Mediator contact phone number
- `OWNER_WHATSAPP`: Mediator WhatsApp number

### File System
- Static files served from `/static` directory
- Image uploads stored in `/static/uploads`
- Templates in `/templates` directory

## Deployment Strategy

### Development
- Flask development server on port 5000
- SQLite database for simplicity
- Debug mode enabled
- File-based image storage

### Production Considerations
- WSGI server deployment (Gunicorn recommended)
- PostgreSQL or MySQL for scalability
- Environment-based configuration
- Proper secret key management
- File upload security measures
- Reverse proxy configuration (nginx)

### Security Features
- Secure filename handling for uploads
- File type validation
- Admin password protection
- Session-based authentication
- Input normalization to prevent inconsistencies

### Scalability Notes
- Database connection pooling configured
- Indexed search fields (plate, chassis)
- Soft deletion for data retention
- Configurable file size limits