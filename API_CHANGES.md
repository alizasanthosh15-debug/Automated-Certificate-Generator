# Backend API Improvements & Changes

## Summary
Complete overhaul of authentication, validation, error handling, and security across all API endpoints.

---

## 🔐 Authentication & Security

### Changes Made:

1. **JWT Token Protection Added to All Routes**
   - `GET /api/certificates/` - List certificates (now protected)
   - `GET /api/certificates/download/<id>` - Download single cert (now protected)
   - `GET /api/certificates/download-zip` - Download all certs zip (now protected)
   - `POST /api/email/send` - Send email notifications (now protected)
   - `POST /api/bulk/upload` - Bulk upload CSV (now protected)
   - All admin routes (already protected, improved)

2. **Improved Token Validation**
   - Better error messages for expired/invalid tokens
   - Proper token format validation (Bearer prefix)
   - Consistent error handling across all decorators

3. **Added functools.wraps to Decorators**
   - Fixes function metadata preservation
   - Better debugging and Flask integration

---

## 📝 Authentication Endpoints

### POST `/api/auth/signup`
**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "role": "user"
}
```

**Improvements:**
- ✅ Email validation (proper format check)
- ✅ Password validation (minimum 6 characters)
- ✅ Name validation (minimum 2 characters)
- ✅ Trim whitespace from inputs
- ✅ Convert email to lowercase
- ✅ Better error messages (no generic errors)

**Response (201 Created):**
```json
{
  "message": "Signup successful",
  "email": "john@example.com",
  "name": "John Doe"
}
```

---

### POST `/api/auth/login`
**Request:**
```json
{
  "email": "john@example.com",
  "password": "password123",
  "role": "user"
}
```

**Improvements:**
- ✅ Input validation
- ✅ Case-insensitive email handling
- ✅ Secure credential comparison
- ✅ Better error messages (generic "invalid email or password" to prevent user enumeration)
- ✅ Admin role validation

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 4,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user"
  }
}
```

---

## 📜 Certificate Endpoints

All certificate endpoints now require JWT token in `Authorization` header:
```
Authorization: Bearer <token>
```

### GET `/api/certificates/`
**List all certificates**

**Response (200 OK):**
```json
[
  {
    "id": 92,
    "name": "Alice",
    "file_path": "/path/to/Alice.pdf",
    "created_at": "2026-01-13 21:04:39"
  }
]
```

**Improvements:**
- ✅ JWT protection added
- ✅ Better error handling
- ✅ Proper date formatting

---

### GET `/api/certificates/download/<int:cert_id>`
**Download single certificate**

**Response:** PDF file (with proper attachment headers)

**Improvements:**
- ✅ JWT protection added
- ✅ Better file path handling (absolute/relative)
- ✅ Path normalization to prevent directory traversal
- ✅ Better error messages

---

### GET `/api/certificates/download-zip`
**Download all certificates as ZIP**

**Response:** ZIP file

**Improvements:**
- ✅ JWT protection added
- ✅ Check for empty certificate directory
- ✅ Better error handling

---

## 📧 Email Endpoints

### POST `/api/email/send`
**Request:**
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "subject": "Certificate Notification"
}
```

**Improvements:**
- ✅ JWT protection added
- ✅ Input validation for email and name
- ✅ Better error responses
- ✅ Logging for debugging

---

## 📤 Bulk Upload Endpoint

### POST `/api/bulk/upload`
**multipart/form-data:**
- `file` (CSV file)

**CSV Format:**
```csv
name
Alice
Bob
Sneha
```

**Improvements:**
- ✅ JWT protection added (requires authentication)
- ✅ File type validation (CSV only)
- ✅ Better CSV parsing error handling
- ✅ Row-by-row error tracking
- ✅ Safe filename generation (prevents directory traversal)
- ✅ Detailed error reporting (returns which rows failed)
- ✅ Unicode encoding validation
- ✅ Proper PDF generation error handling

**Response (200 OK):**
```json
{
  "message": "Bulk upload completed",
  "generated": 3,
  "failed": 0,
  "errors": []
}
```

**Response (400 if some/all failed):**
```json
{
  "message": "Bulk upload completed",
  "generated": 2,
  "failed": 1,
  "errors": ["Row 2: Empty name"]
}
```

---

## 👨‍💼 Admin Endpoints

All admin endpoints require admin JWT token (role="admin").

### GET `/api/admin/users`
**List all users**

**Improvements:**
- ✅ Better error handling with logging
- ✅ Consistent error messages
- ✅ Proper date formatting

---

### DELETE `/api/admin/users/<int:user_id>`
**Delete a user**

**Improvements:**
- ✅ New: Cannot delete your own account (self-delete protection)
- ✅ Better error handling
- ✅ Activity logging

---

### GET `/api/admin/templates`
**List all certificate templates**

### GET `/api/admin/templates/<int:template_id>`
**Get specific template**

### PUT `/api/admin/templates/<int:template_id>`
**Update template**

**Improvements:**
- ✅ Better error handling on all endpoints

---

### GET `/api/admin/certificates`
**List all certificates (admin view)**

### DELETE `/api/admin/certificates/<int:cert_id>`
**Delete a certificate**

---

### GET `/api/admin/activity-logs`
**View all activity logs**

### GET `/api/admin/statistics`
**Get system statistics**
- Total users
- Total certificates
- Total activity logs

---

## 🐛 Bug Fixes

| Issue | Status | Fix |
|-------|--------|-----|
| Missing token validation on some routes | ✅ Fixed | Added `@token_required` decorator |
| Missing input validation | ✅ Fixed | Added email, password, name validation |
| Generic error messages | ✅ Fixed | Better specific error responses |
| Weak password validation | ✅ Fixed | Minimum 6 characters |
| No email format validation | ✅ Fixed | Regex validation |
| CSV parsing errors not handled | ✅ Fixed | Row-by-row error tracking |
| Path traversal vulnerability | ✅ Fixed | Path normalization & validation |
| Admin decorator issues | ✅ Fixed | Added functools.wraps |
| Database connection errors not logged | ✅ Fixed | Added print statements for debugging |
| File encoding issues | ✅ Fixed | Better UTF-8 handling |

---

## 🧪 Testing the API

### 1. Start Backend
```bash
cd backend
python run.py
```

### 2. Signup (Create User)
```powershell
$body = @{
    name = "Test User"
    email = "test@example.com"
    password = "password123"
    role = "user"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/auth/signup" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

$response | ConvertTo-Json
```

### 3. Login (Get Token)
```powershell
$body = @{
    email = "test@example.com"
    password = "password123"
    role = "user"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/auth/login" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

$token = $response.token
$response | ConvertTo-Json
```

### 4. Use Token for Protected Routes
```powershell
$headers = @{ Authorization = "Bearer $token" }

# List certificates
$certs = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/certificates/" `
    -Method GET `
    -Headers $headers

$certs | ConvertTo-Json
```

### 5. Bulk Upload
```powershell
# Create test CSV
$csv = "name`r`nAlice`r`nBob`r`nCharlie"
$csv | Out-File -Encoding UTF8 -Path "test.csv"

# Upload
$headers = @{ Authorization = "Bearer $token" }
$form = @{ file = Get-Item "test.csv" }

$response = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/bulk/upload" `
    -Method POST `
    -Form $form `
    -Headers $headers

$response | ConvertTo-Json
```

---

## 📌 Important Notes

1. **Authentication is now required** for most endpoints
2. **JWT tokens are not cached** - they're validated on each request
3. **Tokens don't expire in current implementation** - add expiration in production
4. **Database must be running** (MySQL on localhost:3306)
5. **admin@example.com user** needs to be created manually if not present

---

## 🔮 Future Improvements

- [ ] Token expiration (add `exp` claim)
- [ ] Token refresh endpoints
- [ ] Rate limiting on auth endpoints
- [ ] Email service integration (SMTP)
- [ ] Audit logging for all operations
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Unit tests for all endpoints
- [ ] Integration tests for workflows
- [ ] Request/response schema validation

---

## 📞 Support

If you encounter any issues:
1. Check MySQL is running: `tasklist | findstr mysql`
2. Check database exists: `mysql -u root -e "SHOW DATABASES;" | findstr acg01`
3. Review backend logs for errors
4. Check that tokens are being sent in `Authorization` header
