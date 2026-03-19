import { useState } from "react";

export const useRecommendations = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getRecommendations = async (query) => {
    try {
      setLoading(true);
      setError(null);

      const res = await fetch(
        `${import.meta.env.VITE_API_URL}/recommend?query=${query}&top_n=5`
      );

      const result = await res.json();
      setData(result.recommendations);

    } catch (err) {
      console.error(err);
      setError("Failed to fetch recommendations");
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, getRecommendations };
};