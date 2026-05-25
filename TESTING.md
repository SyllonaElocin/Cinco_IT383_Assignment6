# Testing Guide

## Local Testing Workflow

### 1. Test User Registration

1. Navigate to `http://localhost:8000/accounts/register/`
2. Fill in the registration form:
   - Username: `newuser`
   - Email: `newuser@example.com`
   - Password: `TestPass123`
   - Confirm Password: `TestPass123`
3. Click "Register"
4. Verify you're logged in and redirected to home

**Expected**: User created successfully, profile created, user logged in

---

### 2. Test User Login

1. If logged in, click "Logout"
2. Navigate to `http://localhost:8000/accounts/login/`
3. Login with `admin` / `admin123`
4. Click "Login"

**Expected**: User logged in, redirected to home, username shown in navbar

---

### 3. Test Album Creation

1. Logged in as admin or any user
2. Click "+ New Album" in navbar
3. Fill in form:
   - Name: `My First Album`
   - Description: `Testing album creation`
   - Public: Check if you want it public
4. Click "Create Album"

**Expected**: Album created, redirected to album detail page, success message shown

---

### 4. Test Album List

1. Navigate to `http://localhost:8000/albums/`
2. Verify albums are displayed in grid
3. If logged in as owner, see "Edit" and "Delete" buttons
4. If admin, see these buttons for all albums

**Expected**: Albums displayed, appropriate buttons visible based on permissions

---

### 5. Test Photo Upload

1. Go to an album detail page
2. Click "+ Add Photo" (if you're the owner or admin)
3. Select an image file
4. Fill in:
   - Title: `Beautiful Sunset`
   - Description: `Taken at the beach`
5. Click "Upload Photo"

**Expected**: Photo uploaded, visible in album grid

---

### 6. Test Photo Edit

1. In album detail, click "Edit" on a photo
2. Change the title or description
3. Click "Update Photo"

**Expected**: Photo metadata updated

---

### 7. Test Photo Delete

1. In album detail, click "Delete" on a photo
2. Confirm deletion

**Expected**: Photo deleted, album refreshed

---

### 8. Test Access Control

### Admin Testing
1. Login as `admin`
2. Go to another user's album
3. Verify you can edit/delete even though you're not the owner

**Expected**: Admin has full access

### Regular User Testing
1. Login as `testuser`
2. Try accessing another user's private album
3. You shouldn't be able to view it

**Expected**: Access denied or not shown in list

---

### 9. Test Public vs Private Albums

1. Create album as public
2. Logout or open in incognito window
3. Verify you can see the public album
4. Try accessing private album of another user
5. Verify you cannot access it

**Expected**: Public visible to all, private visible only to owner/admin

---

### 10. Test Pagination

1. Create 13+ albums
2. Go to album list
3. Verify pagination controls appear
4. Click "Next" and verify next set of albums shown

**Expected**: Pagination working with 12 albums per page

---

### 11. Test Admin Panel

1. Navigate to `http://localhost:8000/admin`
2. Login with admin credentials
3. Verify you can see:
   - User Profiles
   - Albums
   - Photos

**Expected**: Admin panel accessible with all models visible

---

### 12. Test Error Handling

#### Unauthorized Album Edit
1. Login as `testuser`
2. Try to manually access edit URL of admin's album
3. Verify error message shown

**Expected**: "You do not have permission" message

#### Invalid Form Submission
1. Try creating album without name
2. Verify validation error shown

**Expected**: Form shows "required" error

---

### 13. Test Database Operations

```bash
# Check database
python manage.py dbshell

# View all users
select * from auth_user;

# View all albums
select * from album_album;

# View all photos
select * from album_photo;
```

---

### 14. Test Static Files

1. Refresh page (Ctrl+Shift+R)
2. Verify CSS styling is applied
3. Check navbar gradient
4. Verify responsive design on mobile (F12 developer tools)

**Expected**: All styles applied correctly

---

### 15. Test Authentication Redirects

1. Logout
2. Try accessing `http://localhost:8000/albums/my-albums/`
3. Should redirect to login

**Expected**: Redirected to login page

---

## Automated Testing (Optional)

Create `album/tests.py`:

```python
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Album, Photo

class AlbumTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('testuser', 'test@example.com', 'testpass')
        user = User.objects.get(username='testuser')
        Album.objects.create(name='Test Album', owner=user)
    
    def test_album_creation(self):
        album = Album.objects.get(name='Test Album')
        self.assertEqual(album.owner.username, 'testuser')
    
    def test_album_get_photo_count(self):
        album = Album.objects.get(name='Test Album')
        self.assertEqual(album.get_photo_count(), 0)

```

Run tests:

```bash
python manage.py test album
```

---

## Cloudinary Testing

1. Configure Cloudinary credentials in `.env`
2. Upload a photo
3. Verify image displays from Cloudinary URL
4. Check Cloudinary dashboard to see uploaded image

**Expected**: Image stored in Cloudinary, URL working

---

## Performance Testing

### Check Query Count

Add to settings.py (development only):

```python
if DEBUG:
    LOGGING = {
        'version': 1,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        },
    }
```

View database queries in console output.

---

## Security Testing

### CSRF Protection
1. Try submitting form without CSRF token
2. Should get error

### SQL Injection
1. Try entering `'; DROP TABLE album;--` in album name
2. Should be safely escaped

### XSS Protection
1. Try entering `<script>alert('xss')</script>` in album description
2. Should be escaped in template

**Expected**: All attacks blocked

---

## Checklist

- [ ] User registration works
- [ ] User login works
- [ ] Album CRUD works
- [ ] Photo CRUD works
- [ ] Access control enforced
- [ ] Public/private albums work
- [ ] Pagination works
- [ ] Admin panel accessible
- [ ] Static files load
- [ ] Error handling works
- [ ] Authentication redirects work
- [ ] Cloudinary integration works
- [ ] Security measures in place

---

All tests passing = Ready for production deployment! ✅
