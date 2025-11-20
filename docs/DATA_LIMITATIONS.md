# Peloton Data Limitations & Future Work

## Current Status (November 2025)

### What We Have: CSV Export
Peloton's official CSV export provides **summary data** per workout but lacks detailed metrics.

#### ✅ Available in CSV Export
- Workout date and timestamp
- Workout type/fitness discipline (cycling, strength, yoga, etc.)
- Duration (length)
- Total output (kJ)
- Average watts
- Calories burned
- Instructor name
- Personal bests
- Workout trends

#### ❌ NOT Available in CSV Export
- **Second-by-second metrics:**
  - Cadence over time
  - Resistance over time
  - Power output graph
  - Heart rate zones (detailed)
- **Performance curves:**
  - Power curve analysis
  - In-ride performance variations
- **Leaderboard data:**
  - Real-time ranking
  - Comparison with other riders
- **Ride metadata:**
  - Difficulty rating
  - Ride description
  - Music playlist

### What We Could Get from API (Currently Blocked)

The unofficial API provided access to:
- `/api/workout/{id}/performance_graph` - Second-by-second metrics
- `/api/workout/{id}` - Detailed workout metadata
- `/api/ride/{id}/details` - Full ride information
- Real-time leaderboard positions
- Heart rate zone analysis

## Current Workarounds

### Option 1: CSV Analysis (Working Now)
**Pros:**
- Official Peloton feature
- Reliable and won't break
- Good for high-level trends
- Complete historical data

**Cons:**
- No detailed performance metrics
- Summary data only
- Limited analytical depth

### Option 2: Third-Party Integrations
**Strava Sync:**
- If you sync Peloton to Strava, detailed data might be available via Strava API
- Could extract power, heart rate, cadence from Strava activities
- Investigate: https://developers.strava.com/

**Apple Health / Google Fit:**
- May contain more granular health metrics
- Worth exploring for heart rate data

### Option 3: Wait for API Resolution
**Monitor:**
- GitHub issue: https://github.com/philosowaffle/peloton-to-garmin/issues/795
- Peloton may restore API access or release official API
- Community might find workaround

## Analysis Capabilities

### Can Do with CSV Data
1. **Frequency & Consistency**
   - Workouts per week/month
   - Streak tracking
   - Best workout days/times

2. **Output Trends**
   - Total output over time
   - Average watts progression
   - 30-day rolling averages

3. **Workout Patterns**
   - Preferred workout types
   - Duration preferences
   - Instructor analysis

4. **Progress Tracking**
   - Personal bests
   - Milestone achievements
   - Total time/output accumulated

5. **Comparative Analysis**
   - Workout type effectiveness
   - Instructor difficulty comparison
   - Month-over-month progress

### Cannot Do (Without API)
1. **Detailed Performance Analysis**
   - Power zone distribution
   - Cadence patterns
   - Resistance strategy

2. **In-Ride Metrics**
   - Performance variability
   - Energy system usage
   - Pacing analysis

3. **Advanced Modeling**
   - FTP calculation from power curve
   - Fatigue modeling
   - Recovery recommendations

## Future Development Plan

### Phase 1: CSV-Based Analysis ✅ (Current)
- Import and process CSV exports
- Build visualizations for summary metrics
- Track high-level progress

### Phase 2: Enhanced CSV Analysis (Next)
- Statistical analysis of output trends
- Predictive modeling for personal bests
- Workout recommendation engine based on patterns

### Phase 3: Alternative Data Sources (If API stays blocked)
- Strava API integration
- Apple Health data import
- Manual ride data entry tool

### Phase 4: Full API Integration (When available)
- Restore API client functionality
- Implement performance graph analysis
- Build detailed metrics dashboard
- Add second-by-second visualizations

## Action Items for Later

- [ ] Investigate Strava API for detailed metrics
- [ ] Check if Apple Health has granular Peloton data
- [ ] Monitor GitHub issue for API workarounds
- [ ] Research other Peloton third-party integrations
- [ ] Build enhanced analytics with available CSV data
- [ ] Create manual data entry interface for key metrics
- [ ] Set up notification for API endpoint changes

## References

- Peloton CSV Export: https://members.onepeloton.com/profile/workouts
- API Status Discussion: https://github.com/philosowaffle/peloton-to-garmin/issues/795
- Strava API Docs: https://developers.strava.com/
- Project Documentation: `docs/PELOTON_API_STATUS.md`

---

**Last Updated:** November 20, 2025
**Status:** API blocked, using CSV export as primary data source
**Next Review:** Check API status monthly
