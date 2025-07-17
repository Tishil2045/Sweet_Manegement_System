import React, { useState } from 'react';
import axios from 'axios';
import './sweetStyles.css'; // adjust if in /styles/


const AddSweet = () => {
  const [sweet, setSweet] = useState({
    name: '',
    category: '',
    price: '',
    quantity: ''
  });

  const handleChange = (e) => {
    setSweet({ ...sweet, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('http://localhost:5000/sweets', sweet)
      .then(() => {
        alert('Sweet added!');
        setSweet({ name: '', category: '', price: '', quantity: '' });
      })
      .catch(err => {
        alert('Add failed');
        console.error(err);
      });
  };

    const deleteSweet = (id) => {
        if (!window.confirm('Are you sure you want to delete this sweet?')) return;
        axios.delete(`http://localhost:5000/sweets/${id}`)
        .then(() => {
            alert('Sweet deleted!');
            fetchSweets();
        })
        .catch(err => {
            console.error('Delete failed:', err);
            alert('Failed to delete sweet');
        });
    };

    return (
    <div className="container">
        <h2>Add New Sweet</h2>
        <form onSubmit={handleSubmit}>
        <input name="name" type="text" value={sweet.name} onChange={handleChange} placeholder="Name" required />
        <input name="category" type="text" value={sweet.category} onChange={handleChange} placeholder="Category" required />
        <input name="price" type="number" value={sweet.price} onChange={handleChange} placeholder="Price" required />
        <input name="quantity" type="number" value={sweet.quantity} onChange={handleChange} placeholder="Quantity" required />
        <button type="submit">Add Sweet</button>
        <button type="button" onClick={() => deleteSweet(sweet.id)}>Delete</button>
        </form>
    </div>
    );

};

export default AddSweet;
