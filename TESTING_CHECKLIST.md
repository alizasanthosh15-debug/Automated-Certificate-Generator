# Email Refactoring - Testing Checklist

## Pre-Deployment Checklist

### Backend Setup

- [ ] Python packages installed: `pip install -r requirements.txt`
  - [ ] smtplib (standard library)
  - [ ] threading (standard library)
  - [ ] queue (standard library)
  - [ ] logging (standard library)

- [ ] Environment variables configured in `.env`
  - [ ] SMTP_SERVER (set to smtp.gmail.com or custom)
  - [ ] SMTP_PORT (typically 587)
  - [ ] EMAIL_USER (sender email address)
  - [ ] EMAIL_PASS (app-specific password, not account password)

- [ ] Database connected
  - [ ] Can run migrations
  - [ ] Certificates table exists
  - [ ] Templates table exists (for bulk generation)

### Code Verification

- [ ] No syntax errors in modified files
  - [ ] Run: `python -m py_compile app.py app/services/*.py app/routes/*.py`
  - [ ] Check errors: `python -m pytest --collect-only`

- [ ] Imports are correct
  - [ ] Run: `python -c "from app.services.background_task_manager import get_email_queue; print('✅ OK')"`
  - [ ] Run: `python -c "from app.services.email_service import send_emails_background; print('✅ OK')"`

- [ ] Flask app starts without errors
  - [ ] Run: `python run.py`
  - [ ] Look for: "✅ Email queue initialized"
  - [ ] Should see no import/syntax errors

## Functional Testing

### Test 1: Single Certificate with Email

**Steps**:

1. Start the Flask app:
   ```bash
   cd backend
   python run.py
   ```

2. In another terminal or API client (Postman/cURL):
   ```bash
   # Get authentication token first
   POST http://localhost:5000/api/auth/login
   Body: {"email": "test@test.com", "password": "password"}
   ```

3. Save a certificate with email:
   ```bash
   POST http://localhost:5000/api/certificates/save
   Headers: {"Authorization": "Bearer YOUR_TOKEN"}
   Body: {
       "participant_name": "Test User",
       "participant_email": "recipient@example.com",
       "template_id": 1
   }
   Files: {"pdf": <PDF_FILE>}
   ```

**Expected Results**:

- [ ] Response status: `202 Accepted` (NOT 201)
- [ ] Response body contains `"status": "processing"`
- [ ] Response time: < 2 seconds
- [ ] Certificate saved to database
- [ ] PDF file saved to disk
- [ ] In logs:
  ```
  ✅ Email queue initialized
  💾 PDF saved: <filename>.pdf
  ✅ Certificate saved: ID=<id>, Name=Test User
  📬 Queued 1 emails for delivery
  ```

- [ ] Email received (check inbox within 10 seconds)
- [ ] Email contains PDF attachment
- [ ] Email From address is correct
- [ ] Email To address is correct

### Test 2: Check Logging

**Steps**:

1. Monitor logs while running Test 1
2. Look for these log messages:

```
📧 Queueing for delivery
🔌 Establishing new SMTP connection
✅ SMTP connected to smtp.gmail.com:587
✅ Email sent to recipient@example.com
🏁 Email worker processed X emails in Y.XXs
```

**Expected Results**:

- [ ] All log messages appear in order
- [ ] Total email time < 5 seconds from generation
- [ ] No error messages (❌)
- [ ] No "Invalid token" or auth errors

### Test 3: Persistent SMTP Connection

**Steps**:

1. Queue 3 emails in quick succession (use Test 1 three times)
2. Monitor logs and check for SMTP connection

**Expected Results**:

- [ ] "Establishing SMTP connection" appears only ONCE
- [ ] Three "Email sent" messages appear
- [ ] Only one "SMTP connected" message
- [ ] No "SMTP connection closed" until app shutdown
- [ ] Total time for 3 emails: < 10 seconds

### Test 4: Bulk Generation and Email

**Steps**:

1. Create CSV file with test data:
   ```csv
   name,email,event,category
   John Doe,john@example.com,GradCerem,Student
   Jane Smith,jane@example.com,GradCerem,Student
   Bob Johnson,bob@example.com,GradCerem,Student
   ```

2. Upload CSV:
   ```bash
   POST http://localhost:5000/api/preview
   Files: {"file": <CSV_FILE>}
   Headers: {"Authorization": "Bearer YOUR_TOKEN"}
   ```

   Should see:
   - [ ] 3 rows processed
   - [ ] All rows marked "Pending" (no validation errors)
   - [ ] No "Invalid email" messages

3. Generate bulk:
   ```bash
   POST http://localhost:5000/api/generate-bulk
   Headers: {"Authorization": "Bearer YOUR_TOKEN"}
   Body: {
       "participants": [
           {"name": "John Doe", "email": "john@example.com"},
           {"name": "Jane Smith", "email": "jane@example.com"},
           {"name": "Bob Johnson", "email": "bob@example.com"}
       ],
       "template_id": 1
   }
   ```

**Expected Results**:

- [ ] Response status: `202 Accepted`
- [ ] Response body: `"count": 3`
- [ ] Response time: < 1 second
- [ ] Logs show:
  ```
  🛠️ Starting PDF generation for 3 participants...
  ✅ Generated certificate for John Doe
  ✅ Generated certificate for Jane Smith
  ✅ Generated certificate for Bob Johnson
  📊 Generation complete: 3 certificates in X.XXs
  📬 Queueing 3 emails for delivery
  ```

- [ ] 3 certificates saved to database
- [ ] 3 PDFs saved to disk
- [ ] All 3 emails received within 30 seconds
- [ ] Total operation time: < 60 seconds

### Test 5: Error Handling

**Test 5a: Invalid Email**

```bash
POST /api/certificates/save
Body: {
    "participant_name": "Test User",
    "participant_email": "invalid-email",  # ← Invalid
    "template_id": 1
}
```

**Expected**:
- [ ] Certificate still saved (email validation happens at send)
- [ ] Email queued but will fail gracefully
- [ ] Logs show: "⚠️ Skipping invalid-email: ..."
- [ ] No crash/exception

**Test 5b: Missing SMTP Password**

1. Remove EMAIL_PASS from .env
2. Try to send certificate

**Expected**:
- [ ] Request returns 202 (request accepted)
- [ ] Logs show: "❌ SMTP connection failed"
- [ ] No email sent
- [ ] App continues running (doesn't crash)

**Test 5c: Wrong Template ID**

```bash
POST /api/generate-bulk
Body: {
    "participants": [...],
    "template_id": 99999  # ← Doesn't exist
}
```

**Expected**:
- [ ] Falls back to default template
- [ ] Certificates still generated
- [ ] No error returned to user
- [ ] Logs show warning about missing template

### Test 6: Thread Safety

**Steps**:

1. Make 5 concurrent certificate save requests
   ```bash
   for i in {1..5}; do
       curl -X POST http://localhost:5000/api/certificates/save \
           -H "Authorization: Bearer $TOKEN" \
           -F "pdf=@test.pdf" \
           -F "participant_name=User $i" \
           -F "participant_email=user$i@test.com" &
   done
   wait
   ```

**Expected Results**:

- [ ] All 5 requests return 202
- [ ] All 5 get unique certificate IDs
- [ ] All 5 PDFs saved without conflicts
- [ ] All 5 emails queued
- [ ] All 5 emails delivered successfully
- [ ] No race conditions in database
- [ ] Logs appear in order (may be interleaved)

### Test 7: App Shutdown

**Steps**:

1. Start Flask app
2. Queue some emails (don't wait for them to send)
3. Stop Flask app (Ctrl+C)

**Expected Results**:

- [ ] Logs show: "🛑 Shutting down application..."
- [ ] Logs show: "✅ Email queue shutdown complete"
- [ ] Graceful shutdown (no hanging)
- [ ] All queued emails are processed before shutdown
- [ ] No errors on shutdown

## Performance Benchmarks

### Single Email

| Metric | Target | Actual |
|--------|--------|--------|
| Response Time | < 2s | _____ |
| Email Delivery | < 10s | _____ |
| SMTP Connection | Reused | Yes/No |

### Bulk (10 Emails)

| Metric | Target | Actual |
|--------|--------|--------|
| Generation Time | < 5s | _____ |
| Queue Time | < 1s | _____ |
| Email Delivery | < 30s | _____ |
| Total Time | < 35s | _____ |

### Bulk (100 Emails)

| Metric | Target | Actual |
|--------|--------|--------|
| Generation Time | < 30s | _____ |
| Queue Time | < 1s | _____ |
| Email Delivery | < 2min | _____ |
| Total Time | < 3min | _____ |

## Regression Testing

Ensure existing functionality still works:

- [ ] User authentication still works
- [ ] Certificate download still works
- [ ] Template creation still works
- [ ] Database queries still work
- [ ] PDF generation still works
- [ ] File storage still works
- [ ] Error responses still work

## Security Testing

- [ ] SMTP credentials not exposed in logs
  ```bash
  grep -i password backend.log  # Should be empty
  ```

- [ ] Email addresses not logged in plain text (optional)
- [ ] No SQL injection in updates
- [ ] JWT tokens validated correctly
- [ ] Unauthorized users get 401 errors

## Load Testing (Optional)

### Test: 100 Concurrent Bulk Uploads

```bash
# Generate 100 PDFs and upload simultaneously
for i in {1..100}; do
    upload_certificate_async("Test User $i", "user$i@test.com")
done
```

**Monitor**:
- [ ] No out-of-memory errors
- [ ] No "too many open files" errors
- [ ] Database handles load
- [ ] SMTP connection pool works
- [ ] All emails eventually sent

## Cleanup Testing

After all tests:

1. Check disk space usage:
   ```bash
   du -sh backend/app/generated_certificates/
   ```
   - Should see reasonable size

2. Check database:
   ```bash
   SELECT COUNT(*) FROM certificates;
   ```
   - Should match number of generated certificates

3. Clean up test files:
   ```bash
   rm -rf backend/app/generated_certificates/*
   ```

## Sign-Off Checklist

- [ ] All tests passed
- [ ] No errors in logs
- [ ] Performance meets expectations
- [ ] No regressions detected
- [ ] Security verified
- [ ] Documentation complete

**Tested By**: ___________________  
**Date**: ___________________  
**Notes**: 

```
________________________________
________________________________
________________________________
```

---

## Quick Start for Testing

```bash
# 1. Setup
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure
# Edit .env with SMTP settings
cat > .env << EOF
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
EOF

# 3. Run
python run.py

# 4. Test (in another terminal)
# See Test 1-7 above
```

---

**Last Updated**: February 25, 2026
**Checklist Version**: 1.0
