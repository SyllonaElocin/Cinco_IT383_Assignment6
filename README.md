# 📸 Photo Album Management System

A production-ready Django web application for managing and sharing photo albums with cloud storage integration.

## Features

- **User Authentication**: Secure login and registration system
- **Role-Based Access Control (RBAC)**: Admin and regular user roles
- **Album Management**: Create, update, and delete albums
- **Photo Upload**: Upload and organize photos with metadata
- **Cloud Storage**: Cloudinary integration for reliable image hosting
- **Privacy Controls**: Make albums public or private
- **Responsive Design**: Modern Bootstrap 5 UI
- **PostgreSQL Database**: Production-grade database support
- **Security**: HTTPS, CSRF protection, secure cookies

## Tech Stack

- **Backend**: Django 6.0.5
- **Database**: PostgreSQL (SQLite for development)
- **Storage**: Cloudinary
- **Frontend**: Bootstrap 5
- **Deployment**: Render

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (venv)
- Cloudinary account (optional for production)
- PostgreSQL (for production)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/django-photo-album.git
cd django-photo-album
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Environment File

```bash
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux
```

Edit `.env` with your settings:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Initialize Database (Optional)

Create an admin user and sample data:

```bash
python manage.py init_db
```

This creates:
- Admin user: `admin` / `admin123`
- Test user: `testuser` / `testuser123`

### 7. Create Superuser (if not using init_db)

```bash
python manage.py createsuperuser
```

### 8. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

### 9. Access Admin Panel

Visit `http://localhost:8000/admin` with your superuser credentials.

## Configuration

### Cloudinary Setup (Production)

1. Sign up at [Cloudinary](https://cloudinary.com/)
2. Get your Cloud Name, API Key, and API Secret from the dashboard
3. Add to `.env`:

```
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### PostgreSQL Setup (Production)

1. Create a PostgreSQL database
2. Add connection string to `.env`:

```
DATABASE_URL=postgresql://user:password@localhost:5432/photo_album_db
```

## Project Structure

```
django-photo-album/
├── config/                 # Project configuration
│   ├── settings.py        # Django settings
│   ├── urls.py           # URL routing
│   ├── wsgi.py           # WSGI application
│   └── asgi.py           # ASGI application
├── album/                  # Album app
│   ├── models.py         # Album and Photo models
│   ├── views.py          # Class-based views (CBVs)
│   ├── forms.py          # Django forms
│   ├── urls.py           # App URL routing
│   ├── admin.py          # Admin configuration
│   └── management/       # Custom management commands
├── profiles/              # User profile app
│   ├── models.py         # UserProfile model
│   └── admin.py          # Admin configuration
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── home.html         # Home page
│   ├── auth/            # Authentication templates
│   └── album/           # Album templates
├── static/               # Static files (CSS, JS)
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # This file
```

## API Endpoints

### Albums
- `GET /albums/` - List all albums
- `GET /albums/<id>/` - View album details
- `POST /albums/album/create/` - Create new album (requires login)
- `PUT /albums/album/<id>/update/` - Update album (owner/admin only)
- `DELETE /albums/album/<id>/delete/` - Delete album (owner/admin only)

### Photos
- `POST /albums/album/<id>/photo/upload/` - Upload photo (requires login)
- `PUT /albums/photo/<id>/edit/` - Edit photo (owner/admin only)
- `DELETE /albums/photo/<id>/delete/` - Delete photo (owner/admin only)

### Authentication
- `GET /accounts/login/` - Login page
- `POST /accounts/login/` - Login
- `GET /accounts/logout/` - Logout
- `GET /accounts/register/` - Register page

## User Roles

### Regular User (`user`)
- Create their own albums
- Upload photos to their own albums
- View public albums and own private albums
- Edit and delete their own content

### Administrator (`admin`)
- Create/edit/delete any album
- Upload/edit/delete any photo
- Manage user roles
- Access admin panel

## Deployment to Render

### 1. Prepare Repository

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git push -u origin main
```

### 2. Create Render Account

Visit [render.com](https://render.com) and sign up.

### 3. Create PostgreSQL Database

1. Go to Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Configure database settings
4. Note the Internal Connection String

### 4. Deploy Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `photo-album-app`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn config.wsgi:application`

### 5. Set Environment Variables

In Render Dashboard, go to Environment:

```
DEBUG=False
SECRET_KEY=<generate-secure-key>
ALLOWED_HOSTS=<your-render-domain>
DATABASE_URL=<your-postgres-url>
CLOUDINARY_CLOUD_NAME=<your-cloud-name>
CLOUDINARY_API_KEY=<your-api-key>
CLOUDINARY_API_SECRET=<your-api-secret>
```

### 6. Deploy

Click "Deploy" and monitor the logs.

### 7. Initialize Database (Production)

After first deploy:

```bash
render exec python manage.py migrate
render exec python manage.py init_db
```

## Security Considerations

- ✅ Never commit `.env` file (use `.gitignore`)
- ✅ Use strong `SECRET_KEY` in production
- ✅ Set `DEBUG=False` in production
- ✅ Use environment variables for sensitive data
- ✅ Enable HTTPS (enforced in production settings)
- ✅ Use secure cookie settings in production
- ✅ Implement regular database backups

## Troubleshooting

### ModuleNotFoundError: No module named 'decouple'

```bash
pip install python-decouple
```

### ModuleNotFoundError: No module named 'cloudinary'

```bash
pip install cloudinary django-cloudinary-storage
```

### Database connection error

```bash
# Check DATABASE_URL is set correctly in .env
# Verify PostgreSQL is running (if using PostgreSQL)
python manage.py dbshell
```

### Static files not loading

```bash
python manage.py collectstatic --noinput
```

### Cloudinary upload not working

1. Verify Cloudinary credentials in `.env`
2. Check Cloudinary account status and quotas
3. Ensure `cloudinary_storage` is in `INSTALLED_APPS`

## Testing

Run tests with:

```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues or questions, please open an issue on GitHub.

## Changelog

### Version 1.0.0 (Initial Release)
- Album CRUD operations
- Photo upload and management
- User authentication and RBAC
- Cloudinary integration
- Production deployment ready

---

**Happy Photo Sharing! 📸**
