// BaaliMitra Crop Recommendation System - Complete Implementation
// Fully integrated with crop-old functionality

// Element references - Will be populated after DOM loads
let els = {};

const MONTH_TO_SEASON = {
  12: "Winter", 1: "Winter", 2: "Winter",
  3: "Spring",  4: "Spring",  5: "Spring",
  6: "Summer",  7: "Summer",  8: "Summer",
  9: "Autumn", 10: "Autumn", 11: "Autumn",
};

// Map season names to match select options
const SEASON_MAP = {
  "winter": "Winter",
  "spring": "Spring",
  "summer": "Summer",
  "monsoon": "Autumn",  // Map monsoon to Autumn for API
  "autumn": "Autumn"
};

// Crop details for enhanced display
const CROP_DETAILS = {
  rice: { description: 'Ideal for your climate conditions.', season: 'Summer (Kharif)', water: 'High', yield: '3.5-6 tonnes/ha', market: '₹1,800-2,400/qt' },
  maize: { description: 'Excellent choice for summer season.', season: 'Summer (Kharif)', water: 'Medium', yield: '2.5-4 tonnes/ha', market: '₹1,400-1,800/qt' },
  wheat: { description: 'Perfect for winter season.', season: 'Winter (Rabi)', water: 'Medium', yield: '2-4 tonnes/ha', market: '₹2,000-2,500/qt' },
  cotton: { description: 'Well-suited for your soil type.', season: 'Summer (Kharif)', water: 'Medium-High', yield: '15-20 qt/ha', market: '₹5,000-6,200/qt' },
  soybean: { description: 'Suitable for your region.', season: 'Summer (Kharif)', water: 'Medium', yield: '15-20 qt/ha', market: '₹3,600-4,000/qt' },
  chickpea: { description: 'Well-suited for your soil pH.', season: 'Winter (Rabi)', water: 'Low', yield: '8-12 qt/ha', market: '₹4,500-5,500/qt' },
  pigeonpeas: { description: 'Drought-resistant crop.', season: 'Summer (Kharif)', water: 'Low', yield: '6-10 qt/ha', market: '₹6,000-7,000/qt' },
  mothbeans: { description: 'Low maintenance crop.', season: 'Summer (Kharif)', water: 'Low', yield: '4-6 qt/ha', market: '₹8,000-10,000/qt' },
  mungbean: { description: 'Short growing season.', season: 'Summer (Kharif)', water: 'Low', yield: '3-5 qt/ha', market: '₹7,000-9,000/qt' },
  moong: { description: 'Short growing season.', season: 'Summer (Kharif)', water: 'Low', yield: '3-5 qt/ha', market: '₹7,000-9,000/qt' },
  blackgram: { description: 'Nitrogen fixing crop.', season: 'Summer (Kharif)', water: 'Low', yield: '4-6 qt/ha', market: '₹8,000-10,000/qt' },
  lentil: { description: 'Rich in protein.', season: 'Winter (Rabi)', water: 'Low', yield: '6-8 qt/ha', market: '₹6,000-8,000/qt' }
};

// Initialize element references after DOM is loaded
function initializeElements() {
  els = {
    district: document.getElementById("district"),
    season: document.getElementById("season"),
    toggleSeasonal: document.getElementById("toggleSeasonal"),
    btnAutofillSeasonal: document.getElementById("btnAutofill"),
    climateManual: document.getElementById("manual-climate"),
    temperature: document.getElementById("temperature"),
    humidity: document.getElementById("humidity"),
    rainfall: document.getElementById("rainfall"),
    seasonalPreview: document.getElementById("seasonal-preview"),

    toggleSoil: document.getElementById("toggleSoil"),
    soilInputs: document.getElementById("soil-inputs"),
    N: document.getElementById("nitrogen"),
    P: document.getElementById("phosphorus"),
    K: document.getElementById("potassium"),
    ph: document.getElementById("ph"),

    useLocation: document.getElementById("useLocation"),
  };
}

// Initialize the application with enhanced error handling
async function init() {
  try {
    // Initialize element references
    initializeElements();
    
    console.log("[INFO] Initializing crop recommendation system...");
    
    // Load districts and seasons from API
    const res = await fetch("/api/districts");
    if (!res.ok) {
      throw new Error(`API returned ${res.status}`);
    }
    const data = await res.json();

    console.log("[INFO] Districts loaded:", data);

    // Populate districts dropdown
    if (els.district) {
      els.district.innerHTML = '<option value="" selected disabled>Select your district</option>';
      data.districts.forEach(d => {
        const opt = document.createElement("option");
        opt.value = d;
        opt.textContent = d;
        els.district.appendChild(opt);
      });
    }

    // Set current month season
    const month = new Date().getMonth() + 1;
    const autoSeason = MONTH_TO_SEASON[month] || "Summer";
    if (els.season) {
      // Map to HTML select value (Autumn -> monsoon, etc.)
      const seasonToValue = {
        "Winter": "winter",
        "Spring": "spring", 
        "Summer": "summer",
        "Autumn": "monsoon"
      };
      const seasonValue = seasonToValue[autoSeason] || "summer";
      els.season.value = seasonValue;
      console.log(`[INFO] Auto-selected season: ${autoSeason} (${seasonValue})`);
    }

    // Set up event listeners
    setupEventListeners();
    
    // Initialize UI state
    onToggleSeasonal();
    onToggleSoil();
    
    console.log("[INFO] Initialization complete");
    
  } catch (error) {
    console.error("[ERROR] Failed to initialize:", error);
    
    // Fallback: use default districts if API fails
    if (els.district) {
      els.district.innerHTML = `
        <option value="" selected disabled>Select your district</option>
        <option value="Bhaktapur">Bhaktapur</option>
        <option value="Chitawan">Chitawan</option>
        <option value="Dolkha">Dolkha</option>
        <option value="Humla">Humla</option>
        <option value="Ilam">Ilam</option>
        <option value="Jhapa">Jhapa</option>
        <option value="Kathmandu">Kathmandu</option>
        <option value="Lalitpur">Lalitpur</option>
        <option value="Lamjung">Lamjung</option>
        <option value="Manang">Manang</option>
        <option value="Mustang">Mustang</option>
        <option value="Myagdi">Myagdi</option>
        <option value="Nuwakot">Nuwakot</option>
        <option value="Palpa">Palpa</option>
        <option value="Parbat">Parbat</option>
        <option value="Rukum">Rukum</option>
        <option value="Solukhumbu">Solukhumbu</option>
        <option value="Surkhet">Surkhet</option>
        <option value="Syangja">Syangja</option>
      `;
    }
  }
}

function setupEventListeners() {
  // Toggle handlers
  if (els.toggleSeasonal) {
    els.toggleSeasonal.addEventListener("change", onToggleSeasonal);
  }
  if (els.btnAutofillSeasonal) {
    els.btnAutofillSeasonal.addEventListener("click", autofillSeasonalClimate);
  }
  if (els.toggleSoil) {
    els.toggleSoil.addEventListener("change", onToggleSoil);
  }
  if (els.useLocation) {
    els.useLocation.addEventListener("click", useMyLocation);
  }
}

function onToggleSeasonal() {
  if (!els.toggleSeasonal) return;
  
  const seasonal = els.toggleSeasonal.checked;
  if (els.climateManual) {
    els.climateManual.classList.toggle("hidden", seasonal);
  }
  if (els.seasonalPreview) {
    els.seasonalPreview.classList.toggle("hidden", !seasonal);
  }
  if (seasonal) {
    autofillSeasonalClimate();
  }
}

function onToggleSoil() {
  if (!els.toggleSoil) return;
  
  const on = els.toggleSoil.checked;
  if (els.soilInputs) {
    els.soilInputs.classList.toggle("hidden", !on);
  }
}

async function autofillSeasonalClimate() {
  const district = els.district?.value;
  const seasonValue = els.season?.value;
  if (!district || !seasonValue) {
    console.log("[INFO] District or season not selected yet");
    return;
  }

  // Map the season value to API format
  const season = SEASON_MAP[seasonValue.toLowerCase()] || seasonValue;

  try {
    console.log(`[INFO] Fetching climate for ${district}, ${season}...`);
    
    const res = await fetch(`/api/seasonal?district=${encodeURIComponent(district)}&season=${encodeURIComponent(season)}`);
    const data = await res.json();
    
    if (!data.ok) throw new Error(data.error || "No seasonal data");

    const c = data.climate;
    if (els.seasonalPreview) {
      els.seasonalPreview.innerHTML = `
        <i class="fas fa-info-circle"></i>
        <span>Using seasonal climate data for ${district} in ${season}: Temp: ${c.temperature.toFixed(1)}°C, Humidity: ${c.humidity.toFixed(1)}%, Rainfall: ${c.rainfall.toFixed(1)}mm</span>
      `;
      els.seasonalPreview.classList.remove("hidden");
    }
    
    console.log("[INFO] Climate data loaded:", c);
    
  } catch (e) {
    console.error("[ERROR] Climate data error:", e);
    if (els.seasonalPreview) {
      els.seasonalPreview.innerHTML = `
        <i class="fas fa-exclamation-triangle"></i>
        <span>Using default climate data</span>
      `;
    }
  }
}

// Geolocation with Nepal district support
async function useMyLocation(ev) {
  ev.preventDefault();
  if (!navigator.geolocation) {
    showNotification("Geolocation not supported in this browser", "error");
    return;
  }
  
  showNotification("Getting your location...", "info");
  
  navigator.geolocation.getCurrentPosition(async (pos) => {
    const { latitude, longitude } = pos.coords;
    try {
      showLoadingState(true, "Detecting your district...");
      
      const url = `https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json&zoom=10`;
      const resp = await fetch(url, { headers: { "Accept": "application/json" }});
      const data = await resp.json();
      const addr = data.address || {};
      
      // Try several fields that may carry district names
      const candidates = [addr.state_district, addr.county, addr.district, addr.city, addr.town, addr.state];
      let found = candidates.find(Boolean) || "";
      
      if (!found) {
        showNotification("Couldn't detect your district. Please select manually.", "warning");
        return;
      }
      
      // Try to match option ignoring case/spacing
      const options = Array.from(els.district?.options || []).map(o => o.value);
      const match = options.find(o => o.toLowerCase().trim() === found.toLowerCase().trim());
      
      if (match) {
        els.district.value = match;
        
        // Set season from current month
        const month = new Date().getMonth() + 1;
        const autoSeason = MONTH_TO_SEASON[month] || "Summer";
        
        // Map to HTML select value (Autumn -> monsoon, etc.)
        const seasonToValue = {
          "Winter": "winter",
          "Spring": "spring", 
          "Summer": "summer",
          "Autumn": "monsoon"
        };
        const seasonValue = seasonToValue[autoSeason] || "summer";
        els.season.value = seasonValue;
        
        console.log(`[INFO] Location detected: ${found}, Season: ${autoSeason} (${seasonValue})`);
        
        if (els.toggleSeasonal?.checked) {
          autofillSeasonalClimate();
        }
        
        showNotification(`Location detected: ${found}`, "success");
      } else {
        showNotification(`Detected area: ${found}. Please select the closest district manually.`, "info");
      }
    } catch (e) {
      console.error(e);
      showNotification("Failed to detect your location", "error");
    } finally {
      showLoadingState(false);
    }
  }, (err) => {
    showNotification("Location permission denied or unavailable", "error");
    showLoadingState(false);
  }, {
    enableHighAccuracy: true, timeout: 15000, maximumAge: 0
  });
}

function readNumber(el) {
  if (!el) return null;
  const v = parseFloat(el.value);
  return Number.isFinite(v) ? v : null;
}

// Enhanced analysis function with better UX
async function analyzeData() {
  // Get the submit button for updating its state
  const button = event.target;
  const originalText = button.innerHTML;
  button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
  button.disabled = true;
  
  try {
    showLoadingState(true, "Processing your data...");
    
    // Build request payload
    const include_soil = els.toggleSoil?.checked || false;
    const use_seasonal = els.toggleSeasonal?.checked || true;

    // Map season value to API format (monsoon -> Autumn, etc.)
    const seasonValue = els.season?.value || "";
    const season = SEASON_MAP[seasonValue.toLowerCase()] || seasonValue;

    const payload = {
      include_soil,
      use_seasonal,
      district: els.district?.value || "",
      season: season,  // Use mapped season
      top_k: 8
    };

    if (include_soil) {
      payload.soil = {
        N: readNumber(els.N) || 90,
        P: readNumber(els.P) || 40,
        K: readNumber(els.K) || 35,
        ph: readNumber(els.ph) || 6.5,
      };
    }

    if (!use_seasonal) {
      const t = readNumber(els.temperature);
      const h = readNumber(els.humidity);
      const r = readNumber(els.rainfall);
      if (t == null || h == null || r == null) {
        showNotification("Please fill temperature, humidity and rainfall", "warning");
        return;
      }
      payload.climate = { temperature: t, humidity: h, rainfall: r };
    }

    console.log("Sending payload:", payload);

    // Call API with enhanced error handling
    const res = await fetch("/api/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    
    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.error || `API error: ${res.status}`);
    }
    
    const data = await res.json();
    console.log("API response:", data);

    // Render results with enhanced display
    renderResults(data);
    showNotification("Crop recommendations generated successfully!", "success");
    
  } catch (error) {
    console.error("Error analyzing data:", error);
    showNotification(`Error: ${error.message}`, "error");
  } finally {
    // Restore button state
    button.innerHTML = originalText;
    button.disabled = false;
    showLoadingState(false);
  }
}

// Enhanced results rendering with better UI
function renderResults(data) {
  // Update summary info with enhanced formatting
  const used = data.used || {};
  let summaryText = "";
  
  if (used.region && used.region.district) {
    summaryText += `District: ${used.region.district} | Season: ${used.region.season} | `;
  }
  
  if (used.climate) {
    summaryText += `Temperature: ${used.climate.temperature.toFixed(1)}°C | Humidity: ${used.climate.humidity.toFixed(1)}% | Rainfall: ${used.climate.rainfall.toFixed(1)}mm | `;
  }
  
  if (used.soil) {
    summaryText += `N: ${used.soil.N} | P: ${used.soil.P} | K: ${used.soil.K} | pH: ${used.soil.ph}`;
  }

  const summaryElement = document.querySelector('.result-summary span');
  if (summaryElement) {
    summaryElement.innerHTML = `<strong>Based on:</strong> ${summaryText}`;
  }

  // Update crop recommendations with enhanced cards
  const recommendationsContainer = document.querySelector('.crop-recommendations');
  if (recommendationsContainer && data.top) {
    recommendationsContainer.innerHTML = "";
    
    data.top.slice(0, 4).forEach((cropData, index) => {
      const [cropName, prob] = Array.isArray(cropData) ? cropData : [cropData.crop, cropData.match_percentage / 100];
      const matchPercentage = Math.round(prob * 100);
      const cropDetails = CROP_DETAILS[cropName.toLowerCase()] || {
        description: `${cropName} is recommended based on your soil and climate conditions.`,
        season: 'Multiple seasons',
        water: 'Moderate requirements',
        yield: 'Good yield potential',
        market: 'Good market value'
      };
      
      const cropCard = document.createElement('div');
      cropCard.className = 'crop-card result-card';
      cropCard.innerHTML = `
        <div class="crop-image">
          <img src="/static/images/crops/${cropName.toLowerCase().replace(/ /g, '-')}.jpg" 
               alt="${cropName}" 
               onerror="this.src='/static/images/crops/default.jpg'">
          <div class="crop-rank">#${index + 1}</div>
        </div>
        <div class="crop-details">
          <h3>${cropName.charAt(0).toUpperCase() + cropName.slice(1)}</h3>
          <div class="match-tag">
            <span class="match-percent">${matchPercentage}%</span> match
          </div>
          <p>${cropDetails.description}</p>
          <div class="crop-info">
            <div class="info-item">
              <i class="fas fa-calendar"></i>
              <span>${cropDetails.season}</span>
            </div>
            <div class="info-item">
              <i class="fas fa-tint"></i>
              <span>${cropDetails.water}</span>
            </div>
          </div>
          <button class="info-button" onclick="showCropDetails('${cropName.toLowerCase().replace(/\s/g, '')}')">
            <i class="fas fa-info-circle"></i> More Details
          </button>
        </div>
      `;
      recommendationsContainer.appendChild(cropCard);
    });
  }

  // Update polycropping suggestions with enhanced display
  if (data.poly && data.poly.length > 0) {
    updatePolyCroppingSuggestions(data.poly);
  }

  // Show results screen with smooth animation
  showScreen('results-screen');
}

// Enhanced poly-cropping suggestions
function updatePolyCroppingSuggestions(polyData) {
  const container = document.querySelector('.polycropping-container');
  if (!container) return;
  
  container.innerHTML = '';
  
  polyData.slice(0, 2).forEach((combo, i) => {
    const primaryCrop = combo[0][0];
    const companionCrop = combo[1][0];
    const matchPercent = Math.round(combo[0][1] * 100);
    
    const polyPair = document.createElement('div');
    polyPair.className = 'poly-pair';
    polyPair.innerHTML = `
      <div class="poly-crop">
        <img src="/static/images/crops/${primaryCrop.toLowerCase()}.jpg" 
             alt="${primaryCrop}" 
             onerror="this.src='/static/images/crops/default.jpg'">
        <div class="crop-name">${primaryCrop.charAt(0).toUpperCase() + primaryCrop.slice(1)}</div>
      </div>
      <div class="plus-sign">+</div>
      <div class="poly-crop">
        <img src="/static/images/crops/${companionCrop.toLowerCase()}.jpg" 
             alt="${companionCrop}" 
             onerror="this.src='/static/images/crops/default.jpg'">
        <div class="crop-name">${companionCrop.charAt(0).toUpperCase() + companionCrop.slice(1)}</div>
      </div>
      <div class="poly-info">
        <div class="match-tag small">
          <span class="match-percent">${matchPercent}%</span> match
        </div>
        <p>${getCompanionDescription(primaryCrop, companionCrop)}</p>
        <div class="benefits">
          <i class="fas fa-leaf"></i>
          <span>Companion planting benefits</span>
        </div>
      </div>
    `;
    container.appendChild(polyPair);
  });
}

// Enhanced companion planting descriptions
function getCompanionDescription(primary, companion) {
  const descriptions = {
    'rice_moong': 'Moong beans fix nitrogen in soil, benefiting rice growth and improving soil fertility.',
    'rice_lentil': 'Lentils as rotation crop help break pest cycles and add essential nutrients.',
    'maize_beans': 'Classic "Three Sisters" companion planting. Beans fix nitrogen for corn.',
    'maize_pumpkin': 'Pumpkin provides ground cover, reducing weeds and water evaporation.',
    'cotton_moong': 'Moong beans help suppress weeds and improve soil quality naturally.',
    'cotton_sesame': 'Sesame acts as a trap crop for cotton pests while providing additional income.',
    'wheat_mustard': 'Mustard acts as a trap crop for certain pests that affect wheat.',
    'wheat_chickpea': 'Chickpea fixes nitrogen, improving soil fertility for wheat production.',
    'soybean_maize': 'Soybean fixes nitrogen while maize provides support and shade.',
    'groundnut_sunflower': 'Sunflower attracts beneficial insects while groundnut improves soil.'
  };
  
  const key = `${primary.toLowerCase()}_${companion.toLowerCase()}`;
  return descriptions[key] || 
    'These crops work well together based on nutrient needs, growth patterns, and pest management.';
}

// Enhanced notification system
function showNotification(message, type = "info", duration = 5000) {
  // Remove existing notifications
  const existing = document.querySelector('.notification');
  if (existing) existing.remove();
  
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.innerHTML = `
    <div class="notification-content">
      <i class="fas fa-${getNotificationIcon(type)}"></i>
      <span>${message}</span>
      <button onclick="this.parentElement.parentElement.remove()">
        <i class="fas fa-times"></i>
      </button>
    </div>
  `;
  
  document.body.appendChild(notification);
  
  // Auto remove after duration
  setTimeout(() => {
    if (notification.parentElement) {
      notification.remove();
    }
  }, duration);
}

function getNotificationIcon(type) {
  const icons = {
    success: 'check-circle',
    error: 'exclamation-circle',
    warning: 'exclamation-triangle',
    info: 'info-circle'
  };
  return icons[type] || 'info-circle';
}

// Enhanced loading state
function showLoadingState(show, message = "Loading...") {
  let loader = document.querySelector('.global-loader');
  
  if (show && !loader) {
    loader = document.createElement('div');
    loader.className = 'global-loader';
    loader.innerHTML = `
      <div class="loader-content">
        <div class="loader-spinner"></div>
        <p>${message}</p>
      </div>
    `;
    document.body.appendChild(loader);
  } else if (!show && loader) {
    loader.remove();
  } else if (show && loader) {
    loader.querySelector('p').textContent = message;
  }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', init);

// Override the existing analyzeData function
window.analyzeData = analyzeData;