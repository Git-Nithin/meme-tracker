import React, { useState } from "react";
import axios from "axios";

function App() {
  const [tweets, setTweets] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchTweets = async () => {
    setLoading(true);
    try {
      const response = await axios.get("http://localhost:5000/generate-tweets");
      setTweets(response.data.tweets);
    } catch (error) {
      console.error("Error fetching tweets:", error);
    }
    setLoading(false);
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>AI Meme Coin Trend Tracker</h1>
      <button onClick={fetchTweets} disabled={loading}>
        {loading ? "Generating..." : "Generate Tweets"}
      </button>
      {tweets.length > 0 && (
        <div>
          <h2>Generated Tweets:</h2>
          {tweets.map((tweet, index) => (
            <p key={index} style={{ background: "#f4f4f4", padding: "10px", margin: "5px" }}>
              {tweet}
            </p>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
