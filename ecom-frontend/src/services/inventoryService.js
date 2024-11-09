import axios from 'axios';

const inventoryService = axios.create({
  baseURL: 'http://inventory-service:5000', // Communicates with inventory-service within Docker
  timeout: 5000,
});

export default inventoryService;
