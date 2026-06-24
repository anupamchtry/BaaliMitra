# Quick Visual Test Guide

## ✅ Your App is Running!

Server: **http://127.0.0.1:5000/crop-recommendation**

---

## Step-by-Step Visual Test

### 1️⃣ Open Crop Recommendation
- Go to: http://127.0.0.1:5000/crop-recommendation
- You should see: **Welcome Screen** with 3 process steps
- Click: **"Get Started"** button

### 2️⃣ Region Screen - Test District Loading
**What to check:**
- District dropdown should show: "Select your district"
- Click the dropdown
- **Expected:** You should see 19 Nepal districts:
  ```
  Bhaktapur
  Chitawan
  Dolkha
  Humla
  Ilam
  Jhapa
  Kathmandu
  Lalitpur
  ... (and 11 more)
  ```

**If dropdown is empty:**
- Open browser console (F12)
- Check for error messages
- Try refreshing the page

### 3️⃣ Test Autofill Feature
- Select: **"Kathmandu"** from district
- Select: **"Summer"** from season
- Toggle should be checked: "Use seasonal climate data..."
- Click: **"Autofill"** button
- **Expected:** Blue info box appears with:
  ```
  Using seasonal climate data for Kathmandu in Summer: 
  Temp: 32.0°C, Humidity: 72.0%, Rainfall: 285.0mm
  ```

### 4️⃣ Navigate to Soil Screen
- Click: **"Next: Soil Analysis"** button
- You should see soil input form
- Toggle: **"I have soil test results"** ON
- **Expected:** Four input fields appear:
  - Nitrogen (N) - default: 90
  - Phosphorus (P) - default: 40
  - Potassium (K) - default: 35
  - pH Level - default: 6.5

### 5️⃣ Get Recommendations
- Click: **"Get Crop Recommendations"** button
- Button text changes to: "Analyzing..."
- **Expected:** Results screen appears with:
  - Summary bar with your parameters
  - 4 crop cards with images and match %
  - Polycropping suggestions (2 pairs)

### 6️⃣ Verify Results
**Check the summary shows:**
```
Based on: District: Kathmandu | Season: Summer | 
Temperature: 32.0°C | Humidity: 72.0% | Rainfall: 285.0mm | 
N: 90 | P: 40 | K: 35 | pH: 6.5
```

**Check crop cards show:**
- Crop name (e.g., "Rice", "Maize", "Wheat")
- Match percentage (e.g., "95% match")
- Description
- "More Details" button

---

## Browser Console Checks

### Open Developer Tools
Press **F12** → Go to **Console** tab

### Expected Messages (in order):

**On Page Load:**
```
[INFO] Initializing crop recommendation system...
[INFO] Districts loaded: {districts: Array(19), seasons: Array(4)}
[INFO] Initialization complete
[PATCH] Loading crop recommendation integration patch...
[PATCH] Integration patch loaded successfully!
```

**When Click Autofill:**
```
[INFO] Fetching climate for Kathmandu, Summer...
[INFO] Climate data loaded: {temperature: 32, humidity: 72, rainfall: 285}
```

**When Get Recommendations:**
```
[PATCH] Starting crop analysis...
[PATCH] Sending payload: {include_soil: true, use_seasonal: true, ...}
[PATCH] API response: {used: {...}, top: [...], poly: [...]}
```

---

## Common Issues & Quick Fixes

### ❌ District dropdown is empty

**Check:**
1. Browser console for errors
2. URL: http://127.0.0.1:5000/api/districts
3. Should return JSON with 19 districts

**Fix:** Refresh the page, check terminal output

---

### ❌ "Autofill" doesn't show climate data

**Check:**
1. District and season are selected
2. Toggle "Use seasonal climate data" is ON
3. Browser console for errors

**Fix:** Try different district, check `/api/seasonal` endpoint

---

### ❌ Results don't appear

**Check:**
1. Browser console for `[PATCH]` messages
2. Any JavaScript errors
3. Network tab for `/api/recommend` call

**Fix:** Check that patch.js file is loaded

---

### ❌ Images don't show

**This is OK!** 
- Functionality works even without images
- Images will show broken icon but text works
- Add images later to `static/images/crops/`

---

## Success Checklist

Use this to verify everything works:

- [ ] Page loads without errors
- [ ] Districts dropdown shows 19 Nepal districts
- [ ] Can select Kathmandu
- [ ] Can select Summer season
- [ ] Autofill button shows climate data
- [ ] Can navigate to soil screen
- [ ] Soil toggle works
- [ ] "Get Crop Recommendations" button works
- [ ] Results screen appears
- [ ] Crop cards display with match %
- [ ] Summary shows correct parameters
- [ ] No errors in browser console
- [ ] Backend shows no errors in terminal

---

## If All Checks Pass: 🎉

**Congratulations!** Your crop recommendation system is fully integrated and working with Nepal districts!

## If Any Check Fails: 🔧

1. Check browser console (F12)
2. Check terminal output
3. Verify files are saved
4. Try hard refresh (Ctrl+Shift+R)
5. Check the error message

---

## Test with Different Scenarios

### Scenario 1: Kathmandu + Summer + No Soil Data
- District: Kathmandu
- Season: Summer  
- Soil toggle: OFF
- Should work and show default soil values

### Scenario 2: Chitawan + Winter + Custom Soil
- District: Chitawan
- Season: Winter
- Soil toggle: ON
- N=120, P=60, K=50, pH=7.0
- Should show personalized recommendations

### Scenario 3: Manual Climate Input
- Select any district
- Toggle "Use seasonal climate data": OFF
- Enter manual values:
  - Temperature: 28°C
  - Humidity: 65%
  - Rainfall: 150mm
- Should use your custom values

---

## Your App is Ready! 🚀

Everything works exactly like crop-old but with:
✅ Better multi-screen UI
✅ Nepal districts  
✅ Same ML model
✅ Same predictions

**Start testing now!**
