# Quick Start Guide

## Start Backend
```bash
cd backend
python run.py
```
Server runs on: `http://127.0.0.1:5000`

---

## API Credentials

### Test User (Regular)
- Email: `test@example.com`
- Password: `password123`
- Role: `user`

### Admin User (if created)
- Email: `admin@example.com`
- Password: `admin123`
- Role: `admin`

---

## Key API Endpoints

### Public (No Auth Required)
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Get JWT token

### Protected (Requires JWT Token)
- `GET /api/certificates/` - List certificates
- `GET /api/certificates/download/<id>` - Download certificate
- `POST /api/email/send` - Send email notification
- `POST /api/bulk/upload` - Upload CSV and generate certificates

### Admin Only
- `GET /api/admin/users` - List all users
- `GET /api/admin/templates` - List templates
- `DELETE /api/admin/users/<id>` - Delete user
- `GET /api/admin/statistics` - System stats

---

## Example: Complete Workflow

### Step 1: Signup
```powershell
$body = @{
    name = "John Doe"
    email = "john@example.com"
    password = "MyPassword123"
    role = "user"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/auth/signup" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

### Step 2: Login
```powershell
$body = @{
    email = "john@example.com"
    password = "MyPassword123"
    role = "user"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/auth/login" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

$token = $response.token
Write-Host "Token: $token"
```

### Step 3: Use Token for Protected Routes
```powershell
$headers = @{ Authorization = "Bearer $token" }

# List certificates
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/certificates/" `
    -Method GET `
    -Headers $headers
```

### Step 4: Upload CSV with Certificates
```powershell
# Create CSV file
"name`r`nAlice`r`nBob`r`nCharlie" | Out-File -Encoding UTF8 -Path "certs.csv"

# Upload
$headers = @{ Authorization = "Bearer $token" }
$form = @{ file = Get-Item "certs.csv" }

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/bulk/upload" `
    -Method POST `
    -Form $form `
    -Headers $headers
```

---

## Error Handling

### No Token
```
Status: 401
Response: { "error": "No token provided" }
```

### Invalid Token
```
Status: 401
Response: { "error": "Invalid token" }
```

### Admin Access Required
```
Status: 403
Response: { "error": "Admin access required" }
```

### Validation Failed
```
Status: 400
Response: { "error": "Email is required" }
```

---

## Database Status

- Host: `localhost`
- Port: `3306`
- User: `root`
- Password: (empty)
- Database: `acg01`

Check MySQL is running:
```powershell
tasklist | findstr mysql
```

---

## Files Changed

- `app/routes/auth_routes.py` - Added validation, improved error messages
- `app/routes/certificate_routes.py` - Added JWT protection
- `app/routes/bulk_routes.py` - Added JWT protection, improved error handling
- `app/routes/email_routes.py` - Added JWT protection
- `app/routes/admin_routes.py` - Fixed decorators, improved logging

---

## Next Steps

1. ✅ Backend authentication working
2. ⏳ Update frontend to use JWT tokens
3. ⏳ Test all endpoints end-to-end
4. ⏳ Add token expiration
5. ⏳ Deploy to production

---

**For detailed documentation, see `API_CHANGES.md`**
