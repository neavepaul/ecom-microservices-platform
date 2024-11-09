import userService from "./userService";

export const registerUser = async (userData) => {
  try {
    const response = await userService.post('/register', userData);
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : { message: 'Network error' };
  }
};

export const loginUser = async (credentials) => {
  try {
    const response = await userService.post('/login', credentials);
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : { message: 'Network error' };
  }
};
