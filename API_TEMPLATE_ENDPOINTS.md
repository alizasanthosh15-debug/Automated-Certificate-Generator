# Template API Documentation

## Base URL
```
http://127.0.0.1:5000/api
```

## Authentication
All endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

---

## Admin Template Endpoints

### 1. Upload New Template
**Endpoint**: `POST /admin/templates/upload`

**Authentication**: Admin only (requires admin role)

**Request**: `multipart/form-data`

**Form Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | File | Yes | Certificate design image (PNG, JPG, GIF, PDF, SVG) |
| template_name | String | Yes | Name of the template |
| title_text | String | No | Main certificate title (default: "Certificate of Excellence") |
| subtitle_text | String | No | Subtitle text (default: "This certificate is proudly awarded to") |
| border_color | String | No | Hex color code (default: "#0a2540") |
| text_color | String | No | Hex color code (default: "#555555") |
| font_size | Integer | No | Font size in pixels (default: 22) |

**Example Request**:
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('template_name', 'Summer Workshop 2024');
formData.append('title_text', 'Certificate of Completion');
formData.append('subtitle_text', 'For your achievement');
formData.append('border_color', '#667eea');
formData.append('text_color', '#555555');
formData.append('font_size', '24');

fetch('http://127.0.0.1:5000/api/admin/templates/upload', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` },
  body: formData
});
```

**Response** (201 Created):
```json
{
  "message": "Template uploaded successfully",
  "template_id": 15,
  "template_name": "Summer Workshop 2024",
  "template_image_path": "assests/templates/Summer_Workshop_2024_1705942800_image.jpg"
}
```

**Errors**:
- `400`: No file provided or invalid file type
- `401`: No token or invalid token
- `403`: Insufficient permissions (not admin)
- `413`: File too large (> 5MB)
- `500`: Server error

---

### 2. List All Templates (Admin View)
**Endpoint**: `GET /admin/templates`

**Authentication**: Admin only

**Query Parameters**: None

**Example Request**:
```javascript
fetch('http://127.0.0.1:5000/api/admin/templates', {
  headers: { 'Authorization': `Bearer ${token}` }
});
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "Participation",
    "title_text": "Certificate of Participation",
    "subtitle_text": "This certificate is proudly awarded to",
    "border_color": "#0a2540",
    "text_color": "#555555",
    "font_size": 22
  },
  {
    "id": 15,
    "name": "Summer Workshop 2024",
    "title_text": "Certificate of Completion",
    "subtitle_text": "For your achievement",
    "border_color": "#667eea",
    "text_color": "#555555",
    "font_size": 24
  }
]
```

---

### 3. Get Single Template (Admin View)
**Endpoint**: `GET /admin/templates/<template_id>`

**Authentication**: Admin only

**Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| template_id | Integer | ID of the template |

**Example Request**:
```javascript
fetch('http://127.0.0.1:5000/api/admin/templates/15', {
  headers: { 'Authorization': `Bearer ${token}` }
});
```

**Response** (200 OK):
```json
{
  "id": 15,
  "name": "Summer Workshop 2024",
  "title_text": "Certificate of Completion",
  "subtitle_text": "For your achievement",
  "border_color": "#667eea",
  "text_color": "#555555",
  "font_size": 24
}
```

**Errors**:
- `404`: Template not found

---

### 4. Update Template (Admin)
**Endpoint**: `PUT /admin/templates/<template_id>`

**Authentication**: Admin only

**Request Body** (JSON):
```json
{
  "title_text": "New Title",
  "subtitle_text": "New Subtitle",
  "border_color": "#764ba2",
  "text_color": "#ffffff",
  "font_size": 28
}
```

**Example Request**:
```javascript
fetch('http://127.0.0.1:5000/api/admin/templates/15', {
  method: 'PUT',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title_text: "New Title",
    border_color: "#764ba2"
  })
});
```

**Response** (200 OK):
```json
{
  "message": "Template updated successfully"
}
```

---

### 5. Delete Template (Admin)
**Endpoint**: `DELETE /admin/templates/<template_id>`

**Authentication**: Admin only

**Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| template_id | Integer | ID of the template to delete |

**Example Request**:
```javascript
fetch('http://127.0.0.1:5000/api/admin/templates/15', {
  method: 'DELETE',
  headers: { 'Authorization': `Bearer ${token}` }
});
```

**Response** (200 OK):
```json
{
  "message": "Template deleted successfully"
}
```

**Notes**: Deletes the template and its associated image file.

---

## User Template Endpoints

### 1. Get All Active Templates
**Endpoint**: `GET /templates/`

**Authentication**: Required (any authenticated user)

**Query Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| include_inactive | Boolean | Include inactive templates (default: false) |

**Example Request**:
```javascript
fetch('http://127.0.0.1:5000/api/templates/', {
  headers: { 'Authorization': `Bearer ${token}` }
});

// With inactive templates
fetch('http://127.0.0.1:5000/api/templates/?include_inactive=true', {
  headers: { 'Authorization': `Bearer ${token}` }
});
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "Participation",
    "title_text": "Certificate of Participation",
    "subtitle_text": "This certificate is proudly awarded to",
    "border_color": "#0a2540",
    "text_color": "#555555",
    "font_size": 22,
    "template_type": "default",
    "creator_id": null,
    "creator_name": null,
    "template_image_path": null,
    "created_at": "2024-01-15 10:30:00"
  },
  {
    "id": 15,
    "name": "My Custom Template",
    "title_text": "Custom Certificate",
    "subtitle_text": "A custom design",
    "border_color": "#667eea",
    "text_color": "#333333",
    "font_size": 24,
    "template_type": "user_created",
    "creator_id": 3,
    "creator_name": "John Doe",
    "template_image_path": "assests/templates/user_3_1705942800_design.jpg",
    "created_at": "2024-01-20 15:45:00"
  }
]
```

---

### 2. Get User's Templates
**Endpoint**: `GET /templates/my-templates`

**Authentication**: Required

**Query Parameters**: None

**Example Request**:
```javascript
fetch('http://127.0.0.1:5000/api/templates/my-templates', {
  headers: { 'Authorization': `Bearer ${token}` }
});
```

**Response** (200 OK):
```json
[
  {
    "id": 15,
    "name": "My Custom Template",
    "title_text": "Custom Certificate",
    "subtitle_text": "A custom design",
    "border_color": "#667eea",
    "text_color": "#333333",
    "font_size": 24,
    "template_type": "user_created",
    "template_image_path": "assests/templates/user_3_1705942800_design.jpg",
    "created_at": "2024-01-20 15:45:00"
  }
]
```

---

### 3. Create Custom Template
**Endpoint**: `POST /templates/create`

**Authentication**: Required

**Request**: `multipart/form-data`

**Form Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | File | No | Certificate design image (optional) |
| template_name | String | Yes | Name of the template |
| title_text | String | No | Main certificate title |
| subtitle_text | String | No | Subtitle text |
| border_color | String | No | Hex color code |
| text_color | String | No | Hex color code |
| font_size | Integer | No | Font size in pixels |

**Example Request**:
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('template_name', 'My Achievement Template');
formData.append('title_text', 'Achievement Award');
formData.append('border_color', '#FFD700');
formData.append('font_size', '26');

fetch('http://127.0.0.1:5000/api/templates/create', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` },
  body: formData
});
```

**Response** (201 Created):
```json
{
  "message": "Template created successfully",
  "template_id": 16,
  "template_name": "My Achievement Template",
  "template_image_path": "assests/templates/user_3_1705943200_design.jpg"
}
```

**Errors**:
- `400`: Invalid file type or missing required fields
- `401`: No token or invalid token
- `413`: File too large

---

### 4. Update Custom Template
**Endpoint**: `PUT /templates/<template_id>`

**Authentication**: Required (creator only)

**Request Body** (JSON):
```json
{
  "template_name": "Updated Name",
  "title_text": "Updated Title",
  "subtitle_text": "Updated Subtitle",
  "border_color": "#999999",
  "text_color": "#ffffff",
  "font_size": 28
}
```

**Example Request**:
```javascript
fetch('http://127.0.0.1:5000/api/templates/16', {
  method: 'PUT',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    template_name: "Updated Name",
    border_color: "#999999"
  })
});
```

**Response** (200 OK):
```json
{
  "message": "Template updated successfully"
}
```

**Errors**:
- `404`: Template not found or unauthorized (not creator)

---

### 5. Delete Custom Template
**Endpoint**: `DELETE /templates/<template_id>`

**Authentication**: Required (creator only)

**Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| template_id | Integer | ID of the template to delete |

**Example Request**:
```javascript
fetch('http://127.0.0.1:5000/api/templates/16', {
  method: 'DELETE',
  headers: { 'Authorization': `Bearer ${token}` }
});
```

**Response** (200 OK):
```json
{
  "message": "Template deleted successfully"
}
```

**Errors**:
- `404`: Template not found or unauthorized

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created successfully |
| 400 | Bad request (invalid parameters) |
| 401 | Unauthorized (missing/invalid token) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not found |
| 413 | Payload too large |
| 500 | Server error |

---

## Common Response Errors

```json
{
  "error": "No file provided"
}
```

```json
{
  "error": "File type not allowed. Allowed: png, jpg, jpeg, gif, pdf, svg"
}
```

```json
{
  "error": "File too large. Maximum size: 5MB"
}
```

```json
{
  "error": "Template not found or unauthorized"
}
```

---

## File Upload Restrictions

- **Allowed Extensions**: png, jpg, jpeg, gif, pdf, svg
- **Maximum Size**: 5MB
- **Storage Path**: `backend/app/assests/templates/`
- **File Naming**: Automatically secured with `secure_filename()`

---

## Example: Complete Workflow

### Admin uploads template
```javascript
// 1. Admin uploads template
const formData = new FormData();
formData.append('file', certificateImage);
formData.append('template_name', 'Graduation Certificate');
formData.append('title_text', 'Certificate of Graduation');

const response = await fetch('http://127.0.0.1:5000/api/admin/templates/upload', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${adminToken}` },
  body: formData
});

const result = await response.json();
console.log('Template ID:', result.template_id);
```

### User views and uses template
```javascript
// 2. User gets all templates
const templates = await fetch('http://127.0.0.1:5000/api/templates/', {
  headers: { 'Authorization': `Bearer ${userToken}` }
}).then(r => r.json());

// 3. User creates custom template
const userFormData = new FormData();
userFormData.append('file', userDesign);
userFormData.append('template_name', 'My Custom Design');

await fetch('http://127.0.0.1:5000/api/templates/create', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${userToken}` },
  body: userFormData
});

// 4. User views their templates
const myTemplates = await fetch('http://127.0.0.1:5000/api/templates/my-templates', {
  headers: { 'Authorization': `Bearer ${userToken}` }
}).then(r => r.json());
```

---

## Notes

- All timestamps are in UTC format (YYYY-MM-DD HH:MM:SS)
- Template IDs are unique integers
- Template names should be descriptive and unique per user
- Deleting a template also removes the associated image file
- Only authenticated users can access templates
- Admin-only operations are restricted by role
