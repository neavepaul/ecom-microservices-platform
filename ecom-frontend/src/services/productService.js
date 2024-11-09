import axios from 'axios';

const productService = axios.create({
  baseURL: 'http://products-service:5000', // Communicates with products-service within Docker
  timeout: 5000,
});

export default productService;
