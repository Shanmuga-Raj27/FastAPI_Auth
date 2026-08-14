# API Reference

Base URL: `http://127.0.0.1:8000`

Interactive documentation (Swagger UI): `http://127.0.0.1:8000/docs`

---

## Authentication

This API uses **OAuth2 password flow** with **JWT bearer tokens**.

1. Send a `POST /token` request with your username and password
2. Receive an `access_token` in the response
3. Include the token in the `Authorization` header of subsequent requests:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Tokens expire after **15 minutes** by default.

---

## Endpoints

### 1. Register a New User

```http
POST /register/
```

Creates a new user account. The password is automatically hashed before storage.

**Request Body** (`application/json`)

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `username` | string | Yes | Unique, max 100 characters |
| `email` | string | Yes | Valid email format, unique, max 100 characters |
| `password` | string | Yes | Minimum 8 characters |

**Example Request**

```bash
curl -X POST "http://127.0.0.1:8000/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

**Success Response** `201 Created`

```json
{
  "id": 1,
  "email": "john@example.com",
  "username": "john_doe"
}
```

**Error Responses**

| Status | Code | Reason |
|--------|------|--------|
| 400 | `Username already registered` | The username is taken |
| 400 | `Email already registered` | The email is taken |
| 422 | Validation Error | Missing fields or invalid email format |

**Notes**
- The response does **not** include the password
- Passwords are hashed with bcrypt before being saved

---

### 2. Login (Get Access Token)

```http
POST /token
```

Authenticates a user and returns a JWT access token.

**Request Body** (`application/x-www-form-urlencoded`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | Yes | Your registered username |
| `password` | string | Yes | Your account password |

**Example Request**

```bash
curl -X POST "http://127.0.0.1:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=securepass123"
```

**Success Response** `200 OK`

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses**

| Status | Code | Reason |
|--------|------|--------|
| 401 | `Incorrect username or password` | Invalid credentials |

**Notes**
- The request must use `application/x-www-form-urlencoded` format (not JSON)
- Use the Swagger UI "Authorize" button for easy testing
- Copy the `access_token` value for use in the Authorization header

---

### 3. Get Secure Conversation (Protected)

```http
GET /conversation/
```

Returns a protected message. Requires a valid JWT token.

**Headers**

| Header | Value | Required |
|--------|-------|----------|
| `Authorization` | `Bearer <access_token>` | Yes |

**Example Request**

```bash
curl -X GET "http://127.0.0.1:8000/conversation/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Success Response** `200 OK`

```json
{
  "conversation": "This is a secure conversation!",
  "current_user": "john_doe"
}
```

**Error Responses**

| Status | Code | Reason |
|--------|------|--------|
| 401 | `Not authenticated` | Missing or invalid token |
| 401 | `Could not validate credentials` | Token expired or malformed |

---

## Data Models

### User (Response)

Returned after registration or when fetching user data.

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique user identifier |
| `email` | string | User's email address |
| `username` | string | Unique username |

**Example**

```json
{
  "id": 1,
  "email": "john@example.com",
  "username": "john_doe"
}
```

### Token (Response)

Returned after successful login.

| Field | Type | Description |
|-------|------|-------------|
| `access_token` | string | JWT token for authentication |
| `token_type` | string | Always `"bearer"` |

**Example**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### UserIn (Request Body)

Used for user registration.

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `username` | string | Yes | Unique, max 100 chars |
| `email` | string | Yes | Valid email, unique, max 100 chars |
| `password` | string | Yes | Min 8 characters |

**Example**

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123"
}
```

---

## Error Format

All errors return JSON with this structure:

```json
{
  "detail": "Error message here"
}
```

Common HTTP status codes:

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (missing/invalid token) |
| 422 | Unprocessable Entity (invalid input format) |
| 500 | Internal Server Error |

---

## Testing with Swagger UI

The easiest way to test the API is using the built-in Swagger UI:

1. Open `http://127.0.0.1:8000/docs`
2. Click the **Authorize** button (top right)
3. Enter your token as: `Bearer <your_token>`
4. Click **Authorize** and close the dialog
5. Expand any endpoint and click **Try it out**

---

## Rate Limits

No rate limiting is currently implemented. In production, consider adding rate limiting to prevent abuse.
