import React, { useState } from "react";
import "./App.css";

const API_BASE_URL = (process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

function App() {
  const [city, setCity] = useState("");
  const [budget, setBudget] = useState("");
  const [days, setDays] = useState("");
  const [itinerary, setItinerary] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const normalizeItinerary = (data) => {
    if (Array.isArray(data)) {
      return { "Day 1": data };
    }

    if (data && typeof data === "object") {
      if (Array.isArray(data.plan)) {
        return { "Day 1": data.plan };
      }

      const dayEntries = Object.entries(data).filter(([, value]) => Array.isArray(value));
      if (dayEntries.length > 0) {
        return Object.fromEntries(dayEntries);
      }
    }

    return {};
  };

  const generatePlan = async () => {
    if (!city || !budget || !days) {
      alert("Please fill all fields");
      return;
    }

    setLoading(true);
    setError("");
    setItinerary({});

    try {
      const response = await fetch(`${API_BASE_URL}/plan`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          city,
          budget,
          days
        })
      });

      if (!response.ok) {
        const errorPayload = await response.json().catch(() => null);
        const apiMessage =
          errorPayload?.detail?.error ||
          errorPayload?.detail ||
          `Request failed with status ${response.status}`;
        throw new Error(apiMessage);
      }

      const data = await response.json();
      const normalized = normalizeItinerary(data);

      if (Object.keys(normalized).length > 0) {
        setItinerary(normalized);
      } else {
        setError("No itinerary returned from backend.");
      }
    } catch (err) {
      setError(err.message || "Cannot connect to backend. Make sure server is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <div className="container">
        <header className="hero">
          <h1 className="title">TripCraft</h1>
          <p className="subtitle">Real-time Day-wise Travel Itinerary Generator</p>
          
        </header>

        <div className="form-card">
          <div className="field">
            <label htmlFor="city">CITY NAME</label>
            <input
              id="city"
              type="text"
              placeholder="Enter city name"
              value={city}
              onChange={(e) => setCity(e.target.value)}
            />
          </div>

          <div className="field">
            <label htmlFor="budget">BUDGET (Rs)</label>
            <input
              id="budget"
              type="number"
              placeholder="Enter total budget"
              value={budget}
              onChange={(e) => setBudget(e.target.value)}
            />
          </div>

          <div className="field">
            <label htmlFor="days">NUMBER OF DAYS</label>
            <input
              id="days"
              type="number"
              placeholder="Enter number of days"
              value={days}
              onChange={(e) => setDays(e.target.value)}
            />
          </div>

          <button onClick={generatePlan} disabled={loading}>
            {loading ? "Generating..." : "Generate Itinerary"}
          </button>
        </div>

        <div className="results">
          {Object.keys(itinerary).length > 0 && <h2>Your Itinerary</h2>}
          {error && <p className="error">{error}</p>}

          {Object.entries(itinerary).map(([dayLabel, places]) => (
            <div key={dayLabel}>
              <h3 className="day-title">{dayLabel}</h3>
              {places.map((place, index) => (
                <div key={`${dayLabel}-${index}`} className="place-card">
                  <h3>{place.name}</h3>
                  <p>
                    <strong>Category:</strong> {place.category}
                  </p>
                  <p>
                    <strong>Cost:</strong> Rs {place.cost}
                  </p>
                  <p>
                    <strong>Rating:</strong> {place.rating}
                  </p>
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
