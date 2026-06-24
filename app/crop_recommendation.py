import os
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from typing import Dict, List, Tuple
from flask import jsonify

# Paths
DATA_DIR = Path(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'))
MODELS_DIR = Path(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models'))
MODELS_DIR.mkdir(parents=True, exist_ok=True)

CROP_DATA_PATH = DATA_DIR / "Crop_Recommendation.csv"
SEASONAL_PATH = DATA_DIR / "seasonal_averages.csv"
MODEL_PATH = MODELS_DIR / "crop_rf.joblib"

# Defaults if farmer doesn't have soil test
DEFAULT_SOIL = {"N": 90.0, "P": 40.0, "K": 35.0, "ph": 6.5}

# Season mapping by month (1-12)
MONTH_TO_SEASON = {
    12: "Winter", 1: "Winter", 2: "Winter",
    3: "Spring",  4: "Spring",  5: "Spring",
    6: "Summer",  7: "Summer",  8: "Summer",
    9: "Autumn", 10: "Autumn", 11: "Autumn",
}

# Enhanced compatibility for poly-cropping
# -1 = avoid, 0 = neutral, 1 = good, 2 = excellent
COMPAT = {
    ("potato","tomato"): -1, ("tomato","potato"): -1,
    ("maize","beans"): 2, ("rice","lentil"): 1,
    ("maize","pumpkin"): 2, ("wheat","chickpea"): 1,
    ("rice","moong"): 1, ("cotton","moong"): 1,
    ("wheat","mustard"): 1, ("chickpea","wheat"): 1,
    ("rice","blackgram"): 1, ("maize","cowpea"): 2,
    ("cotton","sesame"): 1, ("sugarcane","turmeric"): 1,
    ("soybean","maize"): 1, ("groundnut","sunflower"): 1,
}

# Global variables
_model = None
_seasonal_df = None
_districts = None
_seasons = ["Winter", "Spring", "Summer", "Autumn"]

def load_or_train_model():
    global _model
    if MODEL_PATH.exists():
        _model = joblib.load(MODEL_PATH)
        print(f"[INFO] Loaded model from {MODEL_PATH}")
        return

    # Fallback: train if model not found
    if not CROP_DATA_PATH.exists():
        print(f"[WARNING] Model file not found and dataset missing: {CROP_DATA_PATH}")
        # Create a dummy model for demo purposes
        from sklearn.ensemble import RandomForestClassifier
        _model = RandomForestClassifier(n_estimators=10, random_state=42)
        # Train with dummy data
        dummy_X = np.random.rand(100, 7) * 100
        dummy_y = np.random.choice(['rice', 'maize', 'wheat', 'cotton'], 100)
        _model.fit(dummy_X, dummy_y)
        print("[WARNING] Using dummy model - please provide training data")
        return

    print("[INFO] Training model from data/Crop_Recommendation.csv ...")
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier

    df = pd.read_csv(CROP_DATA_PATH)
    features = ["N","P","K","temperature","humidity","ph","rainfall"]
    X = df[features].values
    y = df["label"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        random_state=42,
        n_jobs=-1
    )
    clf.fit(X_train, y_train)
    joblib.dump(clf, MODEL_PATH)
    print(f"[INFO] Trained and saved model to {MODEL_PATH}")
    _model = clf

def load_seasonal():
    global _seasonal_df, _districts
    if not SEASONAL_PATH.exists():
        print(f"[WARNING] Missing seasonal averages file at {SEASONAL_PATH}")
        # Create dummy data for demo - Nepal districts
        _districts = ["Bhaktapur", "Chitawan", "Dolkha", "Humla", "Ilam", "Jhapa", "Kathmandu", 
                      "Lalitpur", "Lamjung", "Manang", "Mustang", "Myagdi", "Nuwakot", "Palpa", 
                      "Parbat", "Rukum", "Solukhumbu", "Surkhet", "Syangja"]
        _seasonal_df = None
        return

    df = pd.read_csv(SEASONAL_PATH)
    # Normalize expected columns
    cols = {c.lower(): c for c in df.columns}

    def get_col(*names):
        for n in names:
            if n in cols:
                return cols[n]
        raise KeyError(f"Missing any of columns: {names}")

    district_col = get_col("district", "DISTRICT".lower())
    season_col   = get_col("season")
    t2m_col      = get_col("t2m", "T2M".lower())
    prectot_col  = get_col("prectot", "PRECTOT".lower())
    rh2m_col     = get_col("rh2m", "RH2M".lower())

    df["DISTRICT_ORIG"] = df[district_col]
    df["DISTRICT_lower"] = df[district_col].astype(str).str.strip().str.lower()
    df["season_lower"] = df[season_col].astype(str).str.strip().str.lower()
    df["T2M_val"] = pd.to_numeric(df[t2m_col], errors="coerce")
    df["PRECTOT_val"] = pd.to_numeric(df[prectot_col], errors="coerce")
    df["RH2M_val"] = pd.to_numeric(df[rh2m_col], errors="coerce")

    # Drop rows with missing core values
    df = df.dropna(subset=["T2M_val","PRECTOT_val","RH2M_val"])

    # Unique visible district names
    districts_order = (
        df[["DISTRICT_lower","DISTRICT_ORIG"]]
        .drop_duplicates("DISTRICT_lower")
        .sort_values("DISTRICT_ORIG")
    )
    _districts = districts_order["DISTRICT_ORIG"].tolist()
    _seasonal_df = df

def get_climate_for(district: str, season: str) -> Dict[str, float]:
    if _seasonal_df is None:
        # Return default climate data if seasonal data not available - Nepal districts
        defaults = {
            "bhaktapur": {"temperature": 18.0, "humidity": 60.0, "rainfall": 200.0},
            "chitawan": {"temperature": 25.0, "humidity": 55.0, "rainfall": 250.0},
            "dolkha": {"temperature": 10.0, "humidity": 65.0, "rainfall": 180.0},
            "humla": {"temperature": 0.0, "humidity": 60.0, "rainfall": 100.0},
            "ilam": {"temperature": 23.0, "humidity": 70.0, "rainfall": 300.0},
            "jhapa": {"temperature": 24.0, "humidity": 68.0, "rainfall": 280.0},
            "kathmandu": {"temperature": 19.0, "humidity": 62.0, "rainfall": 220.0},
            "lalitpur": {"temperature": 19.0, "humidity": 62.0, "rainfall": 220.0},
            "lamjung": {"temperature": 15.0, "humidity": 65.0, "rainfall": 230.0},
            "manang": {"temperature": 5.0, "humidity": 65.0, "rainfall": 200.0},
            "mustang": {"temperature": 4.0, "humidity": 63.0, "rainfall": 210.0},
            "myagdi": {"temperature": 16.0, "humidity": 60.0, "rainfall": 260.0},
            "nuwakot": {"temperature": 19.0, "humidity": 62.0, "rainfall": 220.0},
            "palpa": {"temperature": 25.0, "humidity": 52.0, "rainfall": 270.0},
            "parbat": {"temperature": 16.0, "humidity": 60.0, "rainfall": 260.0},
            "rukum": {"temperature": 13.0, "humidity": 60.0, "rainfall": 210.0},
            "solukhumbu": {"temperature": -2.0, "humidity": 60.0, "rainfall": 110.0},
            "surkhet": {"temperature": 22.0, "humidity": 55.0, "rainfall": 230.0},
            "syangja": {"temperature": 20.0, "humidity": 58.0, "rainfall": 260.0},
        }
        # Adjust for seasons
        season_adjustments = {
            "winter": {"temperature": -5.0, "humidity": -10.0, "rainfall": -50.0},
            "spring": {"temperature": 5.0, "humidity": 0.0, "rainfall": 20.0},
            "summer": {"temperature": 8.0, "humidity": 15.0, "rainfall": 100.0},
            "autumn": {"temperature": 2.0, "humidity": 5.0, "rainfall": 50.0},
        }
        
        base_climate = defaults.get(district.lower(), {"temperature": 32.0, "humidity": 72.0, "rainfall": 285.0})
        adjustments = season_adjustments.get(season.lower(), {"temperature": 0.0, "humidity": 0.0, "rainfall": 0.0})
        
        return {
            "temperature": max(5.0, base_climate["temperature"] + adjustments["temperature"]),
            "humidity": max(20.0, min(95.0, base_climate["humidity"] + adjustments["humidity"])),
            "rainfall": max(0.0, base_climate["rainfall"] + adjustments["rainfall"])
        }
    
    d = str(district).strip().lower()
    s = str(season).strip().lower()
    row = _seasonal_df[
        (_seasonal_df["DISTRICT_lower"] == d) &
        (_seasonal_df["season_lower"] == s)
    ]
    if row.empty:
        raise ValueError(f"No climate for district='{district}' season='{season}'")
    r = row.iloc[0]
    # PRECTOT is likely mm/day; approximate monthly by multiplying ~30
    return {
        "temperature": float(r["T2M_val"]),
        "humidity":    float(r["RH2M_val"]),
        "rainfall":    float(r["PRECTOT_val"]) * 30.0
    }

def predict_top(
    N: float, P: float, K: float, temperature: float, humidity: float, ph: float, rainfall: float,
    top_k: int = 8
) -> List[Tuple[str, float]]:
    if _model is None:
        # Return dummy predictions
        crops = ['rice', 'maize', 'wheat', 'cotton', 'soybean', 'chickpea', 'pigeonpeas', 'mothbeans']
        probs = [0.95, 0.85, 0.80, 0.75, 0.70, 0.65, 0.60, 0.55]
        return list(zip(crops, probs))
    
    X = np.array([[N,P,K,temperature,humidity,ph,rainfall]])
    probs = _model.predict_proba(X)[0]
    classes = _model.classes_
    idx = np.argsort(probs)[::-1][:top_k]
    return [(classes[i], float(probs[i])) for i in idx]

def poly_suggestions(top_list: List[Tuple[str,float]], combos: int = 2, size: int = 3):
    results = []
    names = [c for c,_ in top_list]
    for start in range(min(3, len(top_list))):
        base = names[start]
        combo = [top_list[start]]
        for c, p in top_list:
            if c == base or len(combo) >= size:
                continue
            score = COMPAT.get((base, c), 0)
            if score >= 0:
                combo.append((c,p))
        if len(combo) >= 2:
            results.append(combo[:size])
        if len(results) >= combos:
            break
    return results

def get_districts_and_seasons():
    """Get available districts and seasons"""
    return {
        "districts": _districts or ["Bhaktapur", "Chitawan", "Dolkha", "Humla", "Ilam", "Jhapa", 
                                     "Kathmandu", "Lalitpur", "Lamjung", "Manang", "Mustang", 
                                     "Myagdi", "Nuwakot", "Palpa", "Parbat", "Rukum", 
                                     "Solukhumbu", "Surkhet", "Syangja"],
        "seasons": _seasons
    }

def get_seasonal_climate(district: str, season: str):
    """Get seasonal climate data for a district and season"""
    try:
        climate = get_climate_for(district, season)
        return {"ok": True, "climate": climate}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def predict_crop(data):
    """
    Generate crop recommendations based on soil and climate data
    This is the main function called by the API
    """
    try:
        if _model is None:
            print("[WARNING] Model not loaded, using dummy predictions")
        
        # Input flags
        include_soil = bool(data.get("include_soil", False))
        use_seasonal = bool(data.get("use_seasonal", True))

        # Soil block
        soil = data.get("soil") or {}
        N  = float(soil.get("N",  DEFAULT_SOIL["N"])) if include_soil else DEFAULT_SOIL["N"]
        P  = float(soil.get("P",  DEFAULT_SOIL["P"])) if include_soil else DEFAULT_SOIL["P"]
        K  = float(soil.get("K",  DEFAULT_SOIL["K"])) if include_soil else DEFAULT_SOIL["K"]
        ph = float(soil.get("ph", DEFAULT_SOIL["ph"])) if include_soil else DEFAULT_SOIL["ph"]

        # Climate block
        if use_seasonal:
            district = data.get("district", "")
            season   = data.get("season", "")
            climate = get_climate_for(district, season)
            temperature = climate["temperature"]
            humidity    = climate["humidity"]
            rainfall    = climate["rainfall"]
        else:
            climate = data.get("climate") or {}
            temperature = float(climate.get("temperature", 32.0))
            humidity    = float(climate.get("humidity", 72.0))
            rainfall    = float(climate.get("rainfall", 285.0))

        top_k = int(data.get("top_k", 8))
        recs = predict_top(N, P, K, temperature, humidity, ph, rainfall, top_k=top_k)
        poly = poly_suggestions(recs, combos=2, size=3)

        return {
            "used": {
                "soil": {"N": N, "P": P, "K": K, "ph": ph, "included": include_soil},
                "climate": {"temperature": temperature, "humidity": humidity, "rainfall": rainfall, "seasonal": use_seasonal},
                "region": {"district": data.get("district"), "season": data.get("season")} if use_seasonal else None
            },
            "top": recs,
            "poly": poly,
            "primary_recommendation": recs[0][0] if recs else "unknown",
            "top_recommendations": [
                {
                    "crop": crop,
                    "match_percentage": round(prob * 100, 1)
                }
                for crop, prob in recs[:5]
            ],
            "status": "success"
        }, 200
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return {"error": str(e)}, 500

# Initialize the module
def initialize():
    try:
        load_or_train_model()
        load_seasonal()
        print(f"[INFO] Districts loaded: {len(_districts) if _districts else 0}")
        print(f"[INFO] Crop recommendation system initialized successfully")
    except Exception as e:
        print(f"[ERROR] Failed to initialize crop recommendation module: {e}")

# Initialize when module is imported
initialize()
