import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Users from './pages/Users';
import Products from './pages/Products';
import Inventory from './pages/Inventory';
import Orders from './pages/Orders';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/users" element={<Users />} />
        <Route path="/products" element={<Products />} />
        <Route path="/inventory" element={<Inventory />} />
        <Route path="/orders" element={<Orders />} />
      </Routes>
    </div>
  );
}

export default App;
