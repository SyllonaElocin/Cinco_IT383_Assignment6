# Deployment Checklist for Render

## Pre-Deployment (Local)

### Code Verification
- [ ] All tests pass locally: `python manage.py test`
- [ ] No syntax errors: `python -m py_compile config/settings.py`
- [ ] All migrations applied: `python manage.py showmigrations`
- [ ] Database working: `python manage.py dbshell`
- [ ] Static files collected: `python manage.py collectstatic --noinput`

### Git Repository
- [ ] Repository initialized: `git init`
- [ ] Files staged: `git add .`
- [ ] Initial commit: `git commit -m "Initial commit"`
- [ ] Branch renamed to main: `git branch -M main`
- [ ] Repository pushed: `git push -u origin main`
- [ ] `.gitignore` includes `.env`, `*.pyc`, `__pycache__/`, `db.sqlite3`
- [ ] No sensitive data in commits

### Environment Configuration
- [ ] `.env` file exists locally with test values
- [ ] `.env.example` exists with placeholders
- [ ] All required variables documented
- [ ] No `.env` in git (check with `git status`)

### Dependencies
- [ ] `requirements.txt` updated: `pip freeze > requirements.txt`
- [ ] All packages installable: `pip install -r requirements.txt`
- [ ] No version conflicts

### Documentation
- [ ] README.md complete and accurate
- [ ] SETUP.md up-to-date
- [ ] Configuration examples provided
- [ ] Deployment instructions clear

---

## Render Setup

### 1. Create Accounts

- [ ] Render account created (render.com)
- [ ] Render API token generated (if needed)

### 2. Create PostgreSQL Database

**Steps:**
1. Go to Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Fill in:
   - **Name**: `photo-album-db`
   - **Database**: `photo_album`
   - **User**: `postgres`
   - **Region**: Select closest region
   - **Plan**: Free (or paid for production)

4. Copy the Internal Connection String
5. Format for Django (if needed):
   ```
   postgresql://[user]:[password]@[host]:[port]/[database]
   ```

- [ ] Database created successfully
- [ ] Connection string copied to secure location
- [ ] No accidental shares of connection string

### 3. Create Web Service

**Steps:**
1. Go to Render Dashboard
2. Click "New +" → "Web Service"
3. Select "Deploy from GitHub"
4. Authorize GitHub and select repository
5. Configure:
   - **Name**: `photo-album-app`
   - **Environment**: `Python 3`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Build Command**:
     ```
     pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
     ```
   - **Start Command**:
     ```
     gunicorn config.wsgi:application
     ```

- [ ] Web service created
- [ ] Build command set correctly
- [ ] Start command set correctly

### 4. Set Environment Variables

In Render Web Service → Environment, add:

```
DEBUG=False
SECRET_KEY=[generate below]
ALLOWED_HOSTS=[render-domain]
DATABASE_URL=[from PostgreSQL service]
CLOUDINARY_CLOUD_NAME=[your cloud name]
CLOUDINARY_API_KEY=[your api key]
CLOUDINARY_API_SECRET=[your api secret]
```

**Generate SECRET_KEY:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

- [ ] SECRET_KEY generated and added
- [ ] DATABASE_URL from PostgreSQL service
- [ ] All Cloudinary variables added (or left empty for local storage)
- [ ] ALLOWED_HOSTS set to Render domain
- [ ] DEBUG set to False
- [ ] All variables marked as non-secret that should be visible

### 5. Configure PostgreSQL Connection

In PostgreSQL service settings:
- [ ] Verify external connection allowed
- [ ] Add web service to access list
- [ ] Copy internal connection string

---

## Deployment Process

### 1. Initial Deploy

- [ ] Click "Deploy" on web service
- [ ] Monitor deployment in logs
- [ ] Wait for "Deployed successfully" message
- [ ] Note the service URL (e.g., `https://photo-album-app.onrender.com`)

### 2. Run Initial Commands

After successful deploy, in Render:

```bash
# Run migrations
render exec photo-album-app python manage.py migrate

# Create admin user
render exec photo-album-app python manage.py createsuperuser

# Initialize database with test data
render exec photo-album-app python manage.py init_db

# Collect static files (if not done in build)
render exec photo-album-app python manage.py collectstatic --noinput
```

- [ ] Migrations ran successfully
- [ ] Admin user created
- [ ] Database initialized
- [ ] Static files collected

### 3. Test Deployed Application

- [ ] Visit `https://[your-domain]` in browser
- [ ] Page loads without errors
- [ ] Admin panel accessible at `/admin`
- [ ] Static files load (CSS, styling)
- [ ] Database connected (no 500 errors)

---

## Post-Deployment

### 1. Verify Functionality

- [ ] User registration works
- [ ] User login works
- [ ] Album creation works
- [ ] Photo upload to Cloudinary works
- [ ] Admin panel accessible
- [ ] Public albums visible
- [ ] Private albums not visible to non-owners

### 2. Security Checks

- [ ] HTTPS enforced
- [ ] No sensitive data in logs
- [ ] Django debug page not showing
- [ ] Error pages generic (not revealing stack traces)
- [ ] SQL errors hidden

### 3. Monitor Logs

In Render dashboard:
- [ ] Check logs for any errors
- [ ] No `SECRET_KEY` or passwords exposed
- [ ] Database connections successful
- [ ] Cloudinary connections successful

### 4. Set Up Custom Domain (Optional)

1. Go to Web Service Settings
2. Click "Add Custom Domain"
3. Enter your domain (e.g., `photos.example.com`)
4. Add DNS CNAME record pointing to Render

- [ ] Domain configured (optional)
- [ ] SSL certificate auto-generated

### 5. Configure Backups

For PostgreSQL service:
- [ ] Automated backups enabled
- [ ] Backup frequency set
- [ ] Backup retention policy set

---

## Rollback Plan

If deployment fails:

1. **Check logs**: View deployment logs in Render
2. **Common issues**:
   - Missing environment variables
   - Database connection string wrong
   - Build command failing (check requirements.txt)
   - Start command not finding gunicorn

3. **Rollback**:
   ```bash
   git revert [commit-hash]
   git push
   ```
   Render will auto-redeploy

4. **Contact Support**: If still failing, contact Render support

---

## Maintenance

### Weekly
- [ ] Check application logs
- [ ] Monitor error rates
- [ ] Verify backups completing

### Monthly
- [ ] Update dependencies: `pip list --outdated`
- [ ] Review security updates
- [ ] Check disk usage (PostgreSQL)

### Quarterly
- [ ] Database optimization
- [ ] Review and clean old data
- [ ] Update Django/dependencies

---

## Important URLs

- **Application**: `https://[your-domain]`
- **Admin Panel**: `https://[your-domain]/admin`
- **Render Dashboard**: `https://dashboard.render.com`
- **Cloudinary Dashboard**: `https://cloudinary.com/console`
- **GitHub Repository**: `https://github.com/[username]/[repo]`

---

## Emergency Contacts

- **Render Support**: support@render.com
- **Django Docs**: https://docs.djangoproject.com
- **Cloudinary Docs**: https://cloudinary.com/documentation

---

## Final Checklist

- [ ] Code deployed to GitHub
- [ ] PostgreSQL database created on Render
- [ ] Web service created on Render
- [ ] All environment variables configured
- [ ] Initial migrations run
- [ ] Admin user created
- [ ] Test data initialized
- [ ] Application tested and working
- [ ] HTTPS verified
- [ ] Admin panel accessible
- [ ] Static files loading
- [ ] Database backups configured
- [ ] Monitoring set up
- [ ] Documentation updated
- [ ] Team informed of deployment

---

**Status**: ✅ Ready for Production Deployment

Once all items are checked, your Photo Album Management System is live on Render!

---

**Deployment Date**: ___________
**Deployed By**: ___________
**Render Domain**: ___________
**Notes**: ___________
