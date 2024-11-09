import axios from 'axios';

const userService = axios.create({
  baseURL: 'http://users-service:5000',
  timeout: 5000,
});

export default userService;
