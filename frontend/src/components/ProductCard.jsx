const ProductCard = ({ product }) => {
  return (
    <div className="product-card">
      <img
        className="product-image"
        src={product["Product Image Url"]}
        alt="product"
      />

      <h4 className="product-name">{product["Product Name"]}</h4>
      <p className="product-price">${product["Product Price"]}</p>
      <p className="product-rating">⭐ {product["Product Rating"]}</p>
    </div>
  );
};

export default ProductCard;