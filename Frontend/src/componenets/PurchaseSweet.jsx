// PurchaseSweet.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";

function PurchaseSweet() {
  const [sweets, setSweets] = useState([]);
  const [sortBy, setSortBy] = useState('');
  const [purchaseQuantities, setPurchaseQuantities] = useState({}); // Track quantity input for each sweet

  const fetchSweets = () => {
    axios.get('http://localhost:5000/sweets')
      .then(res => setSweets(res.data))
      .catch(err => console.error('Error fetching sweets:', err));
  };

  useEffect(() => {
    fetchSweets();
  }, []);

  const handleQuantityChange = (id, value) => {
    setPurchaseQuantities({
      ...purchaseQuantities,
      [id]: value
    });
  };

  const purchaseSweet = (id) => {
    const quantity = parseInt(purchaseQuantities[id]) || 0;

    if (quantity <= 0) {
      alert("Please enter a valid quantity.");
      return;
    }

    axios.post(`http://localhost:5000/sweets/${id}/purchase`, { quantity })
      .then(() => {
        alert("Purchase successful!");
        setPurchaseQuantities(prev => ({ ...prev, [id]: '' })); // clear input
        fetchSweets();
      })
      .catch(err => {
        alert("Purchase failed (maybe out of stock or invalid quantity?)");
        console.error(err);
      });
  };

  const sortedSweets = [...sweets];

  if (sortBy === 'name-asc') {
    sortedSweets.sort((a, b) => a.name.localeCompare(b.name));
  } else if (sortBy === 'name-desc') {
    sortedSweets.sort((a, b) => b.name.localeCompare(a.name));
  } else if (sortBy === 'price-asc') {
    sortedSweets.sort((a, b) => a.price - b.price);
  } else if (sortBy === 'price-desc') {
    sortedSweets.sort((a, b) => b.price - a.price);
  }

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Purchase Sweets</h2>

      <div className="mb-4">
        <label className="mr-2">Sort By:</label>
        <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
          <option value="">None</option>
          <option value="name-asc">Name (A → Z)</option>
          <option value="name-desc">Name (Z → A)</option>
          <option value="price-asc">Price (Low → High)</option>
          <option value="price-desc">Price (High → Low)</option>
        </select>
      </div>

      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>ID</th><th>Name</th><th>Category</th><th>Price</th><th>Available</th><th>Purchase Qty</th><th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {sortedSweets.map(sweet => (
            <tr key={sweet.id}>
              <td>{sweet.id}</td>
              <td>{sweet.name}</td>
              <td>{sweet.category}</td>
              <td>{sweet.price}</td>
              <td>{sweet.quantity}</td>
              <td>
                <input
                  type="number"
                  min="1"
                  max={sweet.quantity}
                  value={purchaseQuantities[sweet.id] || ''}
                  onChange={(e) => handleQuantityChange(sweet.id, e.target.value)}
                  disabled={sweet.quantity <= 0}
                  style={{ width: '60px' }}
                />
              </td>
              <td>
                <button
                  onClick={() => purchaseSweet(sweet.id)}
                  disabled={sweet.quantity <= 0}
                >
                  Purchase
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default PurchaseSweet;
