# Template Upload Feature - Quick Start Guide

## 🎯 Overview
This guide explains how to use the new template upload and creation features in the Certificate Generator application.

## 👨‍💼 For Admin Users

### Upload a New Template

1. **Go to Admin Dashboard**
   - Login with admin credentials (admin@example.com / admin123)
   - Click "Admin Dashboard" from the sidebar or navigate to `/admin-dashboard`

2. **Navigate to Templates Tab**
   - In the Admin Dashboard, click the 🎨 "Templates" tab

3. **Upload New Template**
   - **Drag & Drop Method**: Drag your certificate design file onto the drag-drop area
   - **Click to Browse**: Click "Click to select" link to browse files
   - Supported formats: PNG, JPG, GIF, PDF, SVG
   - Maximum file size: 5MB

4. **Fill Template Details**
   - **Template Name**: Give your template a unique name (required)
   - **Title Text**: The main title that appears on certificates (e.g., "Certificate of Achievement")
   - **Subtitle Text**: Secondary text (e.g., "This certificate is proudly awarded to")
   - **Border Color**: Choose the border color using the color picker
   - **Text Color**: Choose the text color using the color picker
   - **Font Size**: Adjust the font size (12-48 pixels)

5. **Click "Upload Template"**
   - The template is saved to the database
   - Your uploaded image is stored securely
   - All details are available for users to use

6. **View Uploaded Templates**
   - Scroll down to "Existing Templates" section
   - Your newly uploaded template appears with an "admin_upload" badge
   - Edit or delete templates as needed

### Edit Admin-Uploaded Templates

1. In the Templates tab, find your uploaded template
2. Click the ✏️ "Edit" button
3. Modify the template properties in the inline form
4. Click "Save" to confirm changes
5. Click "Cancel" to discard changes

### Delete Admin-Uploaded Templates

1. Find the template in the Templates grid
2. Click the 🗑️ "Delete" button
3. Confirm the deletion
4. The template and associated image file are permanently removed

---

## 👤 For Regular Users

### Create a Custom Certificate Template

1. **Go to Dashboard**
   - Login with your regular account
   - You'll see the main dashboard

2. **Click "Create Custom Template"**
   - From the dashboard cards, click "✨ Create Custom Template"
   - Or navigate to `/create-template`

3. **Step 1: Upload Certificate Design**
   - Drag and drop your certificate design file onto the upload area
   - Or click "Choose File" to browse for a file
   - File will be displayed once selected

4. **Step 2: Customize Template Details**
   - **Template Name** (required): Name your template uniquely
   - **Title Text**: Main certificate title
   - **Subtitle Text**: Subtitle or tagline
   - **Colors**: Select border and text colors
   - **Font Size**: Set the font size in pixels
   - Watch the preview update as you change values

5. **Review Preview**
   - The preview section shows how your template will look
   - Displays your uploaded image with text overlay
   - Make adjustments until satisfied

6. **Click "Create Template"**
   - Template is saved to your account
   - You're redirected to "My Templates" page
   - Success message confirms creation

### Manage Your Templates

1. **Go to "My Templates"**
   - From dashboard, click "📋 My Templates"
   - Or navigate to `/my-templates`

2. **View Your Templates**
   - All templates you've created are displayed in a grid
   - Each card shows:
     - Template image preview
     - Template name and type
     - Template details (title, subtitle, colors)
     - Creation date
     - Action buttons

3. **Edit Your Templates**
   - Click ✏️ "Edit" on any template card
   - Modify the properties in the inline form:
     - Title text
     - Subtitle text
     - Border color
     - Text color
   - Click "Save" to confirm or "Cancel" to discard

4. **Delete Your Templates**
   - Click 🗑️ "Delete" on any template card
   - Confirm the deletion
   - Template is permanently removed

5. **Use a Template**
   - Click 🎯 "Use Template" to generate certificates with that template
   - You'll be taken to the template selection page

### Use Templates to Create Certificates

1. **Browse All Templates**
   - Go to Dashboard
   - Click "🎨 Certificate Templates"
   - Or navigate to `/certificate-templates`

2. **See Available Templates**
   - Default templates provided by the system
   - Admin-uploaded templates (marked with badges)
   - Your custom templates (marked as "user_created")

3. **Select a Template**
   - Click "Use Template" on any template card
   - You'll proceed to create certificates using that template

---

## 🎨 Template Customization Tips

### For Best Results:
1. **Design Size**: Create designs at 1200×800px or larger for best quality
2. **Format**: PNG with transparent background works best
3. **Text Spacing**: Leave space in the template for participant names
4. **Colors**: Test with different border and text colors for contrast

### Color Selection:
- Use the color picker to select exact colors
- Hex codes are displayed for reference
- Test colors with your template for visibility

### Font Sizes:
- Small (12-16px): Fine print, signatures
- Medium (18-28px): Names, dates
- Large (32-48px): Titles, achievements

---

## 🔍 How to Navigate

### From Dashboard
- **Certificate Templates**: Browse all templates
- **Create Custom Template**: Create new templates
- **My Templates**: Manage your templates
- **Create Certificate**: Generate certificates

### For Admins
- **Admin Dashboard**: Access admin features
- **Templates Tab**: Manage all templates in the system

---

## ⚠️ Important Notes

1. **File Uploads**
   - Maximum file size: 5MB
   - Supported formats: PNG, JPG, GIF, PDF, SVG
   - Files are securely stored on the server

2. **Template Ownership**
   - You can only edit/delete your own templates
   - Admin-uploaded templates cannot be deleted by regular users
   - Default system templates cannot be modified

3. **Access Control**
   - Must be logged in to create/manage templates
   - Admin features only available to admin accounts
   - Templates are visible to all authenticated users

4. **Security**
   - All uploads are validated for file type and size
   - Activity logging tracks all admin actions
   - Your templates are stored securely in the database

---

## 🆘 Troubleshooting

### Template Upload Fails
- Check file size (max 5MB)
- Verify file format is PNG, JPG, GIF, PDF, or SVG
- Try clearing browser cache and reloading

### Template Not Appearing
- Refresh the page
- Check if you're logged in
- For admin templates: verify you have admin role

### Changes Not Saved
- Ensure the form is completely filled
- Check for error messages in alerts
- Retry the operation

### Cannot Delete Template
- Only the creator can delete templates
- Default system templates cannot be deleted
- Ask an admin for assistance if needed

---

## 📋 Checklist

### Before Creating Templates
- [ ] Design your certificate template image
- [ ] Ensure image is 1200×800px or larger
- [ ] Plan your color scheme
- [ ] Decide on font sizes
- [ ] Choose descriptive template name

### When Uploading Template
- [ ] File size is under 5MB
- [ ] File format is supported
- [ ] All details are filled correctly
- [ ] Preview looks acceptable
- [ ] You have a backup of the original file

### After Creating Template
- [ ] Verify template appears in "My Templates" or "Existing Templates"
- [ ] Test the template by creating a certificate with it
- [ ] Make adjustments if needed
- [ ] Share feedback or request features

---

## 🚀 Next Steps

Once your templates are created:
1. Use them to generate individual certificates
2. Use them for bulk certificate generation via CSV
3. Share templates with your team (if feature enabled)
4. Download and distribute generated certificates

Enjoy your custom certificate templates! 🎉
