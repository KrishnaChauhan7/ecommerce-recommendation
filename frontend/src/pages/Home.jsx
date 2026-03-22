import { useState } from "react";
import "./Home.css";

function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    try {
      setError("");
      setLoading(true);

      const response = await fetch(
        `http://localhost:8000/recommend?query=${query}&top_n=8`
      );

      if (!response.ok) {
        throw new Error("Server error");
      }

      const data = await response.json();

      if (data.recommendations && data.recommendations.length > 0) {
        setResults(data.recommendations);
      } else {
        setResults([]);
        setError("No recommendations found");
      }

    } catch (err) {
      console.error(err);
      setError("Failed to fetch recommendations");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1 className="title">🛍️ Product Recommendation</h1>

      <div className="search-bar">
        <input
          type="text"
          placeholder="Search products like shoes, shirts..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}

      <div className="grid">
        {results.map((item, index) => (
          <div className="card" key={index}>
            <img
              src={
                item["Product Image Url"] ||
                "https://via.placeholder.com/150"
              }
              alt="product"
            />

            <h3>{item["Product Name"]}</h3>

            <p className="price">₹{item["Product Price"]}</p>

            <p className="rating">⭐ {item["Product Rating"]}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home;