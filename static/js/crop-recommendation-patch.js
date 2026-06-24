// BaaliMitra Crop Recommendation - Integration Patch
// This file patches the main crop-recommendation.js to work with multi-screen UI

console.log("[PATCH] Loading crop recommendation integration patch...");

// Season mapping for API compatibility
const SEASON_MAP_PATCH = {
  "winter": "Winter",
  "spring": "Spring",
  "summer": "Summer",
  "monsoon": "Autumn",
  "autumn": "Autumn"
};

// Crop details for display
const CROP_DETAILS_PATCH = {
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

// Override analyzeData to work with the new UI
window.analyzeDataPatched = async function() {
  const button = event.target;
  const originalText = button.innerHTML;
  button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
  button.disabled = true;
  
  try {
    console.log("[PATCH] Starting crop analysis...");
    
    // Get form elements
    const district = document.getElementById("district")?.value;
    const seasonEl = document.getElementById("season");
    const seasonValue = seasonEl?.value || "";
    const toggleSeasonal = document.getElementById("toggleSeasonal")?.checked !== false;
    const toggleSoil = document.getElementById("toggleSoil")?.checked || false;
    
    // Map season to API format
    const season = SEASON_MAP_PATCH[seasonValue.toLowerCase()] || seasonValue;
    
    // Build payload
    const payload = {
      include_soil: toggleSoil,
      use_seasonal: toggleSeasonal,
      district: district,
      season: season,
      top_k: 8
    };
    
    // Add soil data if toggled
    if (toggleSoil) {
      const readNum = (id, def) => parseFloat(document.getElementById(id)?.value) || def;
      payload.soil = {
        N: readNum("nitrogen", 90),
        P: readNum("phosphorus", 40),
        K: readNum("potassium", 35),
        ph: readNum("ph", 6.5)
      };
    }
    
    // Add manual climate if not using seasonal
    if (!toggleSeasonal) {
      const readNum = (id) => parseFloat(document.getElementById(id)?.value);
      const t = readNum("temperature");
      const h = readNum("humidity");
      const r = readNum("rainfall");
      if (!t || !h || !r) {
        alert("Please fill temperature, humidity and rainfall");
        return;
      }
      payload.climate = { temperature: t, humidity: h, rainfall: r };
    }
    
    console.log("[PATCH] Sending payload:", payload);
    
    // Call API
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
    console.log("[PATCH] API response:", data);
    
    // Update UI with results
    updateResultsUI(data);
    
    // Show results screen
    showScreen('results-screen');
    
  } catch (error) {
    console.error("[PATCH ERROR]:", error);
    alert(`Error: ${error.message}`);
  } finally {
    button.innerHTML = originalText;
    button.disabled = false;
  }
};

// Update results UI
function updateResultsUI(data) {
  const used = data.used || {};
  
  // Update summary
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
  
  const summaryEl = document.querySelector('.result-summary span');
  if (summaryEl) {
    summaryEl.innerHTML = `<strong>Based on:</strong> ${summaryText}`;
  }
  
  // Update crop cards
  const container = document.querySelector('.crop-recommendations');
  if (container && data.top) {
    container.innerHTML = "";
    
    data.top.slice(0, 4).forEach((cropData, index) => {
      const [cropName, prob] = Array.isArray(cropData) ? cropData : [cropData.crop, cropData.match_percentage / 100];
      const matchPercentage = Math.round(prob * 100);
      const details = CROP_DETAILS_PATCH[cropName.toLowerCase()] || {
        description: `${cropName} is recommended.`,
        season: 'Multiple seasons',
        water: 'Moderate',
        yield: 'Good potential',
        market: 'Good value'
      };
      
      const card = document.createElement('div');
      card.className = 'crop-card result-card';
      card.innerHTML = `
        <div class="crop-image">
          <img src="/static/images/crops/${cropName.toLowerCase().replace(/ /g, '-')}.jpg" 
               alt="${cropName}" 
               onerror="this.src='/static/images/crops/default.jpg'">
        </div>
        <div class="crop-details">
          <h3>${cropName.charAt(0).toUpperCase() + cropName.slice(1)}</h3>
          <div class="match-tag">
            <span class="match-percent">${matchPercentage}%</span> match
          </div>
          <p>${details.description}</p>
          <button class="info-button" onclick="showCropDetails('${cropName.toLowerCase().replace(/\s/g, '')}')">
            <i class="fas fa-info-circle"></i> More Details
          </button>
        </div>
      `;
      container.appendChild(card);
    });
  }
  
  // Update polycropping
  if (data.poly && data.poly.length > 0) {
    updatePolycroppingUI(data.poly);
  }
}

// Update polycropping suggestions
function updatePolycroppingUI(polyData) {
  const container = document.querySelector('.polycropping-container');
  if (!container) return;
  
  container.innerHTML = '';
  
  polyData.slice(0, 2).forEach((combo) => {
    if (!combo || combo.length < 2) return;
    
    const primary = combo[0][0];
    const companion = combo[1][0];
    const matchPercent = Math.round(combo[0][1] * 100);
    
    const pair = document.createElement('div');
    pair.className = 'poly-pair';
    pair.innerHTML = `
      <div class="poly-crop">
        <img src="/static/images/crops/${primary.toLowerCase()}.jpg" 
             alt="${primary}" 
             onerror="this.src='/static/images/crops/default.jpg'">
        <div class="crop-name">${primary.charAt(0).toUpperCase() + primary.slice(1)}</div>
      </div>
      <div class="plus-sign">+</div>
      <div class="poly-crop">
        <img src="/static/images/crops/${companion.toLowerCase()}.jpg" 
             alt="${companion}" 
             onerror="this.src='/static/images/crops/default.jpg'">
        <div class="crop-name">${companion.charAt(0).toUpperCase() + companion.slice(1)}</div>
      </div>
      <div class="poly-info">
        <div class="match-tag small">
          <span class="match-percent">${matchPercent}%</span> match
        </div>
        <p>These crops work well together for companion planting.</p>
        <div class="benefits">
          <i class="fas fa-leaf"></i>
          <span>Companion planting benefits</span>
        </div>
      </div>
    `;
    container.appendChild(pair);
  });
}

// Override the global analyzeData function
window.analyzeData = window.analyzeDataPatched;

console.log("[PATCH] Integration patch loaded successfully!");
