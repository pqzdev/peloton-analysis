# Peloton API Status (November 2025)

## API Endpoint Blocked

As of November 2025, Peloton has **blocked the `/auth/login` endpoint** that was previously used for unofficial API access.

**Error message:**
```json
{
  "status": 403,
  "message": "Access forbidden. Endpoint no longer accepting requests."
}
```

This means the unofficial API authentication method is no longer functional.

## Alternative: Official CSV Download

Peloton provides an **official CSV download feature** through their web interface:

### How to Download Your Workout Data

1. **Sign in to Peloton Web**
   - Go to https://members.onepeloton.com/profile/workouts
   - Sign in with your Peloton credentials

2. **Download Workouts**
   - Click the "DOWNLOAD WORKOUTS" button in the top right corner
   - This exports a CSV file with all your workout data

3. **What's Included**
   - Workout type and date
   - Duration and calories
   - Instructor information
   - Personal bests
   - Workout trends
   - And more...

### Important Notes

- **Web Browser Only**: This feature is only available via web browser, not the Peloton App, Bike, or Tread
- **Language Requirement**: Must have your default language set to **English** (not German or Spanish)
- **Official Method**: This is Peloton's official data export feature

## Updated Workflow

Instead of using the API, this project now supports:

1. **Manual Download**: Download CSV from Peloton website
2. **Import Script**: Convert CSV to structured JSON format
3. **Analysis**: Use the same analysis tools on the imported data

See the updated README for instructions on using the CSV import method.

## Future Considerations

- Monitor for any new official Peloton API releases
- Third-party integrations like Strava may continue to work
- CSV export remains the most reliable method for personal data access
