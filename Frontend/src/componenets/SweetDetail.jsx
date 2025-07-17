import React,{ useEffect, useState } from 'react';
import axios from 'axios';
import PurchaseSweet from './PurchaseSweet';

const SweetDetail = () => {
  const [sweets, setSweets] = useState([]);
  const [search, setSearch] = useState({
    name: '',
    category: '',
    min_price: '',
    max_price: ''
  });

  const [sortBy, setSortBy] = useState('');

  const fetchSweets = () => {
    axios.get('http://localhost:5000/sweets')
      .then(res => setSweets(res.data))
      .catch(err => console.error('Error fetching sweets:', err));
  };

  useEffect(() => {
    fetchSweets();
  }, []);

  const handleSearchChange = (e) => {
    setSearch({ ...search, [e.target.name]: e.target.value });
  };

  const handleSearch = () => {
    const params = new URLSearchParams();
    Object.entries(search).forEach(([key, value]) => {
      if (value) params.append(key, value);
    });

    axios.get(`http://localhost:5000/sweets/search?${params.toString()}`)
      .then(res => setSweets(res.data))
      .catch(err => console.error('Search error:', err));
  };

    const handleReset = () => {
        setSearch({ name: '', category: '', min_price: '', max_price: '' });
        fetchSweets();
    };

  const sortedSweets = [...sweets]; // make a copy

    if (sortBy === 'name-asc') {
    sortedSweets.sort((a, b) => a.name.localeCompare(b.name));
    } else if (sortBy === 'name-desc') {
    sortedSweets.sort((a, b) => b.name.localeCompare(a.name));
    } else if (sortBy === 'price-asc') {
    sortedSweets.sort((a, b) => a.price - b.price);
    } else if (sortBy === 'price-desc') {
    sortedSweets.sort((a, b) => b.price - a.price);
    }

  return(
    <div>
        <h2 className="text-xl font-bold mb-4">Sweet Inventory</h2>

        {/* Search Form */}
        <div style={{ marginBottom: '20px' }}>
            <input type="text" name="name" placeholder="Name" value={search.name} onChange={handleSearchChange} />
            <input type="text" name="category" placeholder="Category" value={search.category} onChange={handleSearchChange} />
            <input type="number" name="min_price" placeholder="Min Price" value={search.min_price} onChange={handleSearchChange} />
            <input type="number" name="max_price" placeholder="Max Price" value={search.max_price} onChange={handleSearchChange} />
            <button onClick={handleSearch}>Search</button>
            <button onClick={handleReset}>Reset</button>
            
        </div>

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


        {/* Table */}
        <table border="1" cellPadding="10">
            <thead>
            <tr>
                <th>ID</th><th>Name</th><th>Category</th><th>Price</th><th>Quantity</th>
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

                </tr>
            ))}
            </tbody>
        </table>
    </div>
  )

}

export default SweetDetail