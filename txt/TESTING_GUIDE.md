# Quick Test - Verify Crop Recommendation Integration

## Test 1: Check if Flask app starts
```powershell
python run.py
```
Expected: Server starts without errors on http://localhost:5000 or http://127.0.0.1:5000

## Test 2: Check API endpoints
Open these URLs in your browser:

1. **Health check**:  
   `http://localhost:5000/api/health`  
   Expected: `{"status": "ok", "message": "..."}`

2. **Districts list**:  
   `http://localhost:5000/api/districts`  
   Expected: `{"districts": [...], "seasons": [...]}`

3. **Model info**:  
   `http://localhost:5000/api/model-info`  
   Expected: `{"model_loaded": true, ...}`

## Test 3: Test seasonal climate data
`http://localhost:5000/api/seasonal?district=Varanasi&season=Summer`  
Expected: `{"ok": true, "climate": {"temperature": ..., "humidity": ..., "rainfall": ...}}`

## Test 4: Test crop recommendation page
`http://localhost:5000/crop-recommendation`  
Expected: Your beautiful multi-screen UI loads!

## Test 5: Full workflow test
1. Go to `http://localhost:5000/crop-recommendation`
2. Click "Get Started"
3. Select "Varanasi" as district
4. Select "Summer" as season  
5. Click "Autofill" button
   - You should see: "Using seasonal climate data for Varanasi in Summer: Temp: XX°C..."
6. Click "Next: Soil Analysis"
7. Toggle "I have soil test results" ON
8. Click "Get Crop Recommendations"
9. You should see the results screen with crop cards!

## Test 6: Check browser console
Press F12 to open developer tools, go to Console tab.

You should see:
```
[INFO] Initializing crop recommendation system...
[INFO] Districts loaded: {...}
[PATCH] Loading crop recommendation integration patch...
[PATCH] Integration patch loaded successfully!
```

When you click "Get Crop Recommendations":
```
[PATCH] Starting crop analysis...
[PATCH] Sending payload: {...}
[PATCH] API response: {...}
```

## Common Issues & Solutions

### Issue: "Cannot GET /crop-recommendation"
**Solution**: Make sure routes are registered in `app/__init__.py`

### Issue: "API error: 404"
**Solution**: Check that blueprint is registered: `app.register_blueprint(api_bp)`

### Issue: Districts dropdown is empty
**Solution**: 
1. Check `/api/districts` endpoint
2. Verify `app/crop_recommendation.py` initializes correctly
3. Check data files in `data/` folder

### Issue: "showScreen is not defined"
**Solution**: That's from the inline script in the HTML, it should work fine

### Issue: Crops not showing
**Solution**: Check browser console - the API call should work even if images are missing

## Success Criteria

✅ Flask app starts without errors  
✅ `/api/districts` returns district list  
✅ `/api/seasonal` returns climate data  
✅ Crop recommendation page loads  
✅ "Autofill" button loads climate data  
✅ "Get Crop Recommendations" shows results  
✅ Results show crop names and match percentages  
✅ No errors in browser console  

If all checks pass, your integration is complete! 🎉
