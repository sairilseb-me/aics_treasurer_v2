import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    headers: {
        Accept: 'application/json',
    }
})

axiosInstance.interceptors.request.use(
    config => {
        const token = localStorage.getItem('token');
        if (token){
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config
    },
    (error) => {
        return Promise.reject(error);
      }
)

axiosInstance.interceptors.response.use( 
        response => response, 
        error => {
        console.log('Error:', error.response);

        // Check if error.response is defined
        if (error.response) {
            if (error.response.status === 401) {
                localStorage.removeItem('token');
                localStorage.removeItem('username');
                window.location.href = '/auth/login';
            }
        } else if (error.request) {
            // The request was made but no response was received
            console.log('Error Request:', error.request);
        } else {
            // Something happened in setting up the request that triggered an Error
            console.log('Error Message:', error.message);
        }

        return Promise.reject(error);
        }
)

export default axiosInstance;
