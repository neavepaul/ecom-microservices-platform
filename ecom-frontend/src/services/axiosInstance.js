import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'https://psychic-space-broccoli-4grw4p459jgfgpw-5000.app.github.dev/',
  timeout: 5000,
});

export default axiosInstance;
