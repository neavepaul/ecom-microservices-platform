import axios from 'axios';

const orderService = axios.create({
  baseURL: 'http://orders-service:5000', // Communicates with orders-service within Docker
  timeout: 5000,
});

export default orderService;
