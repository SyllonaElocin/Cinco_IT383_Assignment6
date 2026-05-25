# Quick Start Guide

## First Time Setup (5 minutes)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Create Environment File

Copy the example environment file:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

### Step 3: Run Migrations

Create the database tables:

```bash
python manage.py migrate
```

### Step 4: Initialize Database

Create admin and test users with sample data:

```bash
python manage.py init_db
```

**Output:**
```
✓ Admin user created: username="admin", password="admin123"
✓ Test user created: username="testuser", password="testuser123"
✓ Sample album created

Test Credentials:
  Admin - username: "admin", password: "admin123"
  User  - username: "testuser", password: "testuser123"
```

### Step 5: Start Development Server

```bash
python manage.py runserver
```

Open your browser to `http://localhost:8000`

---

## Default Test Accounts

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| User | testuser | testuser123 |

---

## Common Tasks

### Create a New Admin User

```bash
python manage.py createsuperuser
```

### Access Admin Panel

Navigate to: `http://localhost:8000/admin`

### Collect Static Files (Production)

```bash
python manage.py collectstatic --noinput
```

### Make Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create an Empty Migration

```bash
python manage.py makemigrations --empty album
```

---

## Troubleshooting

### Port 8000 Already in Use

Use a different port:

```bash
python manage.py runserver 8001
```

### Database Locked Error

Delete and recreate:

```bash
rm db.sqlite3
python manage.py migrate
python manage.py init_db
```

### Static Files Not Loading

```bash
python manage.py collectstatic --noinput
```

### Module Import Errors

Reinstall dependencies:

```bash
pip install --upgrade -r requirements.txt
```

---

## Project Features

✅ User authentication and registration
✅ Role-based access control (RBAC)
✅ Photo album CRUD operations
✅ Cloud storage with Cloudinary
✅ Responsive design with Bootstrap 5
✅ PostgreSQL support for production
✅ Security best practices

---

## Next Steps

1. **Customize**: Modify templates and styles in `templates/` and `static/`
2. **Deploy**: Follow the Render deployment instructions in README.md
3. **Extend**: Add more features and customize the models
4. **Test**: Write tests in `tests.py` files

---

For more information, see the main [README.md](README.md) file.
