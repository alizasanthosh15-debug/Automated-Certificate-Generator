# Template Upload & User Template Creation Feature - Implementation Summary

## Overview
Implemented a comprehensive template management system that allows:
1. **Admin Users**: Upload certificate templates via drag-and-drop interface
2. **Regular Users**: Create custom certificate templates with their own designs
3. **All Users**: Access both default templates and user-created/admin-uploaded templates

## Changes Made

### 1. Database Schema Updates
**File**: `backend/database_migrations.sql`

Added new columns to the `templates` table:
- `template_type` ENUM('default', 'admin_upload', 'user_created') - Categorizes template source
- `creator_id` INT - Foreign key linking to the user who created the template
- `template_image_path` VARCHAR(500) - Path to the uploaded template image
- `is_active` BOOLEAN - Flag to enable/disable templates

Modified the templates table definition to include proper foreign key constraints.

### 2. Backend Routes

#### Admin Template Upload Route
**File**: `backend/app/routes/admin_routes.py`

Added new endpoints for admin template management:

- **POST** `/api/admin/templates/upload`
  - Accepts multipart form data with file and template details
  - Validates file type (PNG, JPG, GIF, PDF, SVG)
  - Max file size: 5MB
  - Saves file to `app/assests/templates/`
  - Stores template metadata in database
  - Logs activity to activity_logs table
  
- **DELETE** `/api/admin/templates/<template_id>`
  - Removes template and associated image file
  - Only admins can delete templates
  - Logs deletion activity

Key features:
- File upload validation
- Secure filename handling using `werkzeug.utils.secure_filename`
- File size validation
- Admin-only access via `@verify_admin` decorator
- Activity logging for audit trail

#### User Template Routes
**File**: `backend/app/routes/template_routes.py` (NEW)

Created new blueprint with endpoints for user template management:

- **GET** `/api/templates/`
  - Returns all active templates (default, admin-uploaded, user-created)
  - Includes creator information
  - Can filter by status

- **GET** `/api/templates/my-templates`
  - Returns templates created by the authenticated user
  - Filtered by `creator_id` and `template_type='user_created'`

- **POST** `/api/templates/create`
  - Allows users to create custom templates
  - Accepts optional file upload
  - Stores user as creator
  - Returns template ID and confirmation

- **PUT** `/api/templates/<template_id>`
  - Allows users to edit their own templates
  - Verifies ownership before allowing updates
  - Updates template properties

- **DELETE** `/api/templates/<template_id>`
  - Allows users to delete their own templates
  - Removes associated image file
  - Verifies ownership

### 3. Frontend Components

#### A. Admin Dashboard Enhancement
**File**: `frontend/src/pages/AdminDashboard.jsx` & `.css`

Added template upload section with:
- **Drag & Drop Area**: Visual feedback, active state styling
- **File Input**: Click to select alternative to drag-and-drop
- **Template Form**: Input fields for:
  - Template Name
  - Title Text
  - Subtitle Text
  - Border Color (color picker)
  - Text Color (color picker)
  - Font Size
- **Existing Templates Grid**: Shows all templates with:
  - Template image preview
  - Edit functionality (inline form)
  - Delete button (with confirmation)
  - Type badge (default/admin_upload)
- **State Management**:
  - `dragActive`: For drag-and-drop visual feedback
  - `uploadingTemplate`: Loading state during upload
  - `newTemplate`: Form data for new template
- **Upload Function**: Multipart form data submission with progress feedback

#### B. Create Template Page (NEW)
**File**: `frontend/src/pages/CreateTemplate.jsx` & `.css`

Dedicated page for users to create custom templates with:
- **Step 1**: Upload certificate design via drag-and-drop
- **Step 2**: Customize template details
  - Template name
  - Title and subtitle text
  - Color selection with hex code display
  - Font size adjustment
- **Preview Section**: Live preview of the template
- **Form Actions**: Create or Cancel buttons
- **Responsive Design**: Works on mobile and desktop

Key features:
- Image preview using `URL.createObjectURL()`
- Form validation (required fields)
- Error handling with user-friendly messages
- Automatic navigation on successful creation

#### C. My Templates Page (NEW)
**File**: `frontend/src/pages/MyTemplates.jsx` & `.css`

Displays user's custom templates with:
- **Header**: Title, description, and "Create New" button
- **Empty State**: Helpful message when no templates exist
- **Templates Grid**: Card-based layout showing:
  - Template image
  - Template name and type badge
  - Quick details (title, subtitle, colors)
  - Creation date
  - Action buttons (Edit, Delete, Use)
- **Edit Mode**: Inline editing of template properties
- **Delete Confirmation**: Prevents accidental deletion

#### D. Certificate Templates Page Updates
**File**: `frontend/src/pages/CertificateTemplates.jsx` & `.css`

Enhanced to:
- Fetch templates from backend API instead of hardcoding
- Display both default and user-created templates
- Add "Create Custom Template" button
- Add "My Templates" button
- Show template type badges
- Fallback to default templates if API fails
- Load state handling

#### E. Dashboard Updates
**File**: `frontend/src/pages/Dashboard.jsx`

Added new navigation cards:
- 🎨 Certificate Templates
- ✨ Create Custom Template
- 📋 My Templates

Expanded dashboard-cards section from 3 to 6 cards.

### 4. App Routing
**File**: `frontend/src/App.jsx`

Added new protected routes:
- `/certificate-templates` - Browse all templates
- `/create-template` - Create custom template
- `/my-templates` - Manage user's templates

All routes are protected with ProtectedRoute component (requires authentication).

### 5. Backend Integration
**File**: `backend/app/__init__.py`

Registered new template_routes blueprint:
```python
from app.routes.template_routes import template_bp
app.register_blueprint(template_bp, url_prefix="/api/templates")
```

## File Structure

### Backend
```
backend/app/
├── routes/
│   ├── admin_routes.py (UPDATED)
│   └── template_routes.py (NEW)
└── assests/
    └── templates/ (NEW - stores uploaded images)
```

### Frontend
```
frontend/src/pages/
├── CertificateTemplates.jsx (UPDATED)
├── CreateTemplate.jsx (NEW)
├── CreateTemplate.css (NEW)
├── MyTemplates.jsx (NEW)
├── MyTemplates.css (NEW)
├── Dashboard.jsx (UPDATED)
└── AdminDashboard.jsx (UPDATED)
```

## Key Features

### 1. Drag & Drop Upload
- Visual feedback on drag enter/leave
- Active state styling
- File validation before upload
- File size limitation (5MB)

### 2. File Management
- Secure filename handling
- Organized storage in `app/assests/templates/`
- Automatic cleanup on template deletion
- Relative path storage in database

### 3. Access Control
- Admin-only operations for admin uploads
- User can only modify their own templates
- Public read access to templates (with authentication)

### 4. Activity Logging
- All admin template actions logged
- Includes user, action type, and description
- Timestamp for audit trail

### 5. Responsive Design
- Mobile-friendly drag-and-drop areas
- Grid layouts that adapt to screen size
- Touch-friendly buttons and inputs

## API Endpoints Summary

### Admin Endpoints
- `POST /api/admin/templates/upload` - Upload template (Admin only)
- `DELETE /api/admin/templates/<id>` - Delete template (Admin only)
- `GET /api/admin/templates` - List templates (Admin only)
- `PUT /api/admin/templates/<id>` - Update template (Admin only)

### User Endpoints
- `GET /api/templates/` - Get all active templates
- `GET /api/templates/my-templates` - Get user's templates
- `POST /api/templates/create` - Create custom template
- `PUT /api/templates/<id>` - Update custom template
- `DELETE /api/templates/<id>` - Delete custom template

## Migration Steps

1. **Database Update**:
   ```bash
   # Run in MySQL Workbench or phpMyAdmin:
   ALTER TABLE templates ADD COLUMN template_type ENUM('default', 'admin_upload', 'user_created') DEFAULT 'default';
   ALTER TABLE templates ADD COLUMN creator_id INT;
   ALTER TABLE templates ADD COLUMN template_image_path VARCHAR(500);
   ALTER TABLE templates ADD COLUMN is_active BOOLEAN DEFAULT TRUE;
   ALTER TABLE templates ADD FOREIGN KEY (creator_id) REFERENCES users(user_id) ON DELETE CASCADE;
   ```

2. **Create Upload Directory**:
   ```bash
   mkdir -p backend/app/assests/templates
   chmod 755 backend/app/assests/templates
   ```

3. **Install Dependencies**: No new dependencies required (uses werkzeug which is already included)

4. **Test the Features**:
   - Admin: Login and go to Admin Dashboard > Templates tab
   - User: Login and go to Dashboard > Create Custom Template
   - View: All users can browse templates at Certificate Templates

## Security Considerations

1. **File Upload**: 
   - Validates MIME types
   - Restricts file extensions
   - Enforces file size limits
   - Uses secure filename generation

2. **Access Control**:
   - All template operations require authentication
   - Admin operations require admin role
   - Users can only modify their own templates

3. **Activity Logging**:
   - All admin actions logged
   - Includes timestamp and user info
   - Enables audit trail

## Error Handling

- File validation errors with clear messages
- Ownership verification for user templates
- Proper HTTP status codes (401, 403, 404, 500)
- User-friendly error alerts in frontend

## Future Enhancements

1. Template sharing between users
2. Template categories/tags
3. Template preview before creation
4. Batch template management
5. Template versioning
6. Analytics on template usage
7. Template marketplace/gallery
