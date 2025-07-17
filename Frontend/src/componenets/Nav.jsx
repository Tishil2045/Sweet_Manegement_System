import React from "react";
import { Link } from "react-router-dom";
import './sweetStyles.css';

function Nav() {
  return (
    <div className="navbar">
      <h1>Sweet Shop</h1>
      <ul className="nav-list">
        <li><Link to='/'>Sweet-Details</Link></li>
        <li><Link to='/sweets'>Add-Sweet</Link></li>
        <li><Link to='/sweets/purchase'>Sweet-Purchase</Link></li>
        <li><Link to='/sweets/restock'>Sweet-Restock</Link></li>
      </ul>
    </div>
  );
}

export default Nav;
