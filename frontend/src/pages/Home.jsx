import SearchBar from "../Components/SearchBar";
import ProductList from "../Components/ProductList";
import Loader from "../Components/Loader";
import ErrorMessage from "../Components/ErrorMessage";
import { useRecommendations } from "../hooks/useRecommendations";

const Home = () => {
  const { data, loading, error, getRecommendations } = useRecommendations();

  return (
    <div className="container">
      <h1 className="title">🛍 Product Recommendation</h1>

      <SearchBar onSearch={getRecommendations} />

      {loading && <Loader />}
      {error && <ErrorMessage message={error} />}
      {data.length > 0 && <ProductList products={data} />}
    </div>
  );
};

export default Home;