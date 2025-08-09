# EcoVolt Motors - Solar Vehicle Website

A complete Flask web application for a solar vehicle and energy storage company.

## 📁 Project Structure

```
ecovolt-motors-website/
├── app.py              # Main Flask application
├── templates/          # HTML template files
│   ├── base.html      # Base template with common layout
│   ├── index.html     # Homepage
│   ├── services.html  # Services page
│   ├── technology.html # Technology page
│   └── contact.html   # Contact page
└── README.md          # This file
```

## 🚀 Quick Setup

### Step 1: Create Project Folder
```bash
mkdir ecovolt-motors-website
cd ecovolt-motors-website
```

### Step 2: Create Templates Folder
```bash
mkdir templates
```

### Step 3: Copy Files
Copy all the provided files into their respective locations:
- `app.py` in the root folder
- All `.html` files in the `templates/` folder

### Step 4: Install Flask
```bash
pip install flask
```

### Step 5: Run the Application
```bash
python app.py
```

### Step 6: View the Website
Open your browser and go to: **http://localhost:5000**

## 📄 Available Pages

- **Homepage** (/) - Main landing page with hero section, services overview, FAQ
- **Services** (/services) - Detailed service offerings with pricing tables  
- **Technology** (/technology) - Technical specifications and innovation timeline
- **Contact** (/contact) - Contact form, business information, and locations

## ✨ Features

- ✅ Responsive design (mobile-friendly)
- ✅ Interactive FAQ toggles
- ✅ Working contact forms
- ✅ Professional solar/automotive theme
- ✅ Template inheritance for easy maintenance
- ✅ Real images from Unsplash (loads automatically)

## 🛠️ Technologies Used

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Template Engine**: Jinja2
- **Images**: Unsplash (CDN)

## 🌐 Browser Support

- Chrome ✅
- Firefox ✅
- Safari ✅
- Edge ✅
- Mobile browsers ✅

## 🔧 Customization

To modify the website:

1. **Edit content**: Modify the HTML files in `templates/` folder
2. **Change styles**: Edit the CSS in the `{% block extra_css %}` sections
3. **Add new pages**: Create new HTML files and add routes in `app.py`
4. **Modify base layout**: Edit `templates/base.html` for site-wide changes

## 📝 File Contents Summary

### Main Application (`app.py`)
- Flask routes for all pages
- Simple structure with render_template calls
- Debug mode enabled for development

### Templates
- **`base.html`**: Common layout, navigation, footer
- **`index.html`**: Homepage with hero section, services grid, FAQ
- **`services.html`**: Service categories with pricing tables
- **`technology.html`**: Technical specs and innovation timeline
- **`contact.html`**: Contact form and location information

## 🎨 Design Features

- **Modern gradient header** with blue theme
- **Grid-based layouts** for responsive design
- **Interactive elements** (hover effects, form validation)
- **Professional color scheme** (blue, green, white)
- **Clean typography** with proper hierarchy

## 🚦 Development Tips

1. **Hot Reload**: Flask debug mode automatically reloads when you save files
2. **Template Inheritance**: All pages extend `base.html` for consistency
3. **Mobile First**: CSS is designed to be mobile-responsive
4. **Image Loading**: All images load from Unsplash CDN automatically

## 🌍 Production Deployment

For production deployment, consider:

- Using a production WSGI server (gunicorn, uWSGI)
- Setting up a reverse proxy (nginx)
- Configuring environment variables
- Setting up SSL certificates
- Using a proper database for contact forms

### Example Production Setup
```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 📋 Manual File Creation Steps

Since the zip file didn't work, follow these steps to create all files manually:

### 1. Create the main application file:
- Create `app.py` and copy the Flask application code

### 2. Create the templates directory:
```bash
mkdir templates
```

### 3. Create each template file:
- `templates/base.html` - Base template with navigation
- `templates/index.html` - Homepage with all sections
- `templates/services.html` - Services page with pricing
- `templates/technology.html` - Technology page with timeline
- `templates/contact.html` - Contact page with form

### 4. Copy the respective code into each file from the artifacts provided above

## 🆘 Troubleshooting

**Issue**: Flask not found
**Solution**: `pip install flask`

**Issue**: Templates not loading
**Solution**: Make sure `templates/` folder exists and contains all HTML files

**Issue**: Images not loading
**Solution**: Check internet connection (images load from Unsplash)

**Issue**: Port already in use
**Solution**: Change port in `app.py` from 5000 to another number (e.g., 8000)

## 📞 Support

If you need help:
1. Check that all files are in the correct locations
2. Ensure Flask is installed: `pip list | grep Flask`
3. Verify Python version: `python --version` (3.7+ recommended)

---

**Created by AI Assistant** - EcoVolt Motors Solar Vehicle Website
**Framework**: Flask + HTML/CSS/JavaScript
**Theme**: Solar vehicles and energy storage systems