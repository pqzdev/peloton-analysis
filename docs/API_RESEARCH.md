# Peloton API Research

## Overview

Peloton does not have an official public API, but the web and mobile apps use internal APIs that can be accessed.

## Authentication

The Peloton API uses cookie-based authentication:

1. **Login endpoint**: `POST https://api.onepeloton.com/auth/login`
   - Request body:
     ```json
     {
       "username_or_email": "your_email",
       "password": "your_password"
     }
     ```
   - Returns session cookie and user info

2. **Session management**:
   - Session cookie: `peloton_session_id`
   - Include in subsequent requests via Cookie header

## Key Endpoints (To Research)

### User Profile
- `GET /api/me` - Get current user info
- `GET /api/user/{user_id}` - Get specific user profile

### Workouts
- `GET /api/user/{user_id}/workouts` - Get workout history
  - Query params: `page`, `limit`, `joins` (for detailed metrics)
- `GET /api/workout/{workout_id}` - Get specific workout details
- `GET /api/workout/{workout_id}/performance_graph` - Get second-by-second metrics

### Ride Details
- `GET /api/ride/{ride_id}/details` - Get ride (class) information
- `GET /api/instructor/{instructor_id}` - Get instructor info

### Performance Metrics
- `GET /api/user/{user_id}/overview` - Get user stats overview
- Power zones, heart rate zones (endpoints TBD)

## Rate Limiting

- No official documentation
- Best practice: Implement exponential backoff
- Cache aggressively to minimize requests

## Notes

- All endpoints are HTTPS only
- Base URL: `https://api.onepeloton.com`
- User-Agent header recommended
- Some endpoints require specific joins/filters via query params

## Next Steps

1. Test authentication flow
2. Explore available workout data structure
3. Document full endpoint responses
4. Identify pagination mechanisms
5. Map out all available metrics

## Resources

- Check GitHub for community projects: `peloton api python`
- Look for Postman collections or API docs
- Review network traffic from Peloton web app
