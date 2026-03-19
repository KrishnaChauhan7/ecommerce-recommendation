import ProductCard from "./ProductCard";

const ProductList = ({ products }) => {
  return (
    <div className="product-grid">
      {products.map((item, index) => (
        <ProductCard key={index} product={item} />
      ))}
    </div>
  );
};

export default ProductList;