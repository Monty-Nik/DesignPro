const API = process.env.VUE_APP_API_URL || 'http://lifestealer86.ru/api-shop';

const handleResponse = async (response) => {
    console.log('Response status:', response.status);
    console.log('Response URL:', response.url);

    let data;
    try {
        data = await response.json();
        console.log('Response data:', data);
    } catch (e) {
        console.error('Failed to parse JSON:', e);
        throw new Error('Неверный формат ответа от сервера');
    }

    if (!response.ok) {
        let errorMessage = 'Ошибка запроса';

        if (data.error) {
            errorMessage = data.error.message || errorMessage;

            if (data.error.code) {
                errorMessage += ` (Код: ${data.error.code})`;
            }

            if (data.error.errors) {
                const errors = Object.entries(data.error.errors)
                    .map(([field, msgs]) => `${field}: ${msgs.join(', ')}`)
                    .join('; ');
                errorMessage += ` | ${errors}`;
            }
        }

        const error = new Error(errorMessage);
        error.status = response.status;
        error.data = data;
        throw error;
    }

    return data;
};

const getHeaders = (includeAuth = true) => {
    const headers = {
        'Content-Type': 'application/json;charset=utf-8',
    };

    if (includeAuth) {
        const token = localStorage.getItem('myAppToken');
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
    }

    return headers;
};


export const loginRequest = (credentials) => {
    console.log(' Login request to:', `${API}/login`);
    console.log(' Email:', credentials.email || credentials.username);

    const requestBody = {
        email: credentials.email || credentials.username,
        password: credentials.password
    };

    return fetch(`${API}/login`, {
        method: 'POST',
        headers: getHeaders(false),
        body: JSON.stringify(requestBody),
    })
        .then(handleResponse)
        .then((result) => {
            console.log(' Login success:', result);
            if (result.data && result.data.user_token) {
                return result.data.user_token;
            } else if (result.user_token) {
                return result.user_token;
            } else {
                throw new Error('Токен не найден в ответе сервера');
            }
        });
};

export const registerRequest = (userData) => {
    console.log(' Register request to:', `${API}/signup`);
    console.log(' FIO:', userData.fio);

    const requestBody = {
        fio: userData.fio,
        email: userData.email,
        password: userData.password
    };

    return fetch(`${API}/signup`, {
        method: 'POST',
        headers: getHeaders(false),
        body: JSON.stringify(requestBody),
    })
        .then(handleResponse)
        .then((result) => {
            console.log(' Register success:', result);

            if (result.data && result.data.user_token) {
                return result.data.user_token;
            } else if (result.user_token) {
                return result.user_token;
            } else {
                throw new Error('Токен не найден в ответе сервера');
            }
        });
};

export const getProducts = () => {
    console.log(' Fetching products from:', `${API}/products`);

    return fetch(`${API}/products`, {
        method: 'GET',
        headers: getHeaders(false),
    })
        .then(handleResponse)
        .then(result => {
            console.log(' Products fetched:', result);
            return result.data || [];
        });
};

export const getCart = () => {
    console.log('🛒 Fetching cart from:', `${API}/cart`);

    return fetch(`${API}/cart`, {
        method: 'GET',
        headers: getHeaders(true),
    })
        .then(handleResponse)
        .then(result => {
            console.log(' Cart fetched:', result);

            const cartData = result.data || [];

            if (cartData.length > 0) {
                console.log(' Cart item example:', cartData[0]);
                console.log(' Available fields:', Object.keys(cartData[0]));
            }

            return cartData;
        });
};

export const addToCart = (productId) => {
    console.log('➕ Adding to cart:', `${API}/cart/${productId}`);

    return fetch(`${API}/cart/${productId}`, {
        method: 'POST',
        headers: getHeaders(true),
    })
        .then(handleResponse)
        .then(result => {
            console.log(' Added to cart:', result);
            return result.data || result;
        });
};

export const removeFromCart = (cartItemId) => {
    console.log(' Removing from cart:', `${API}/cart/${cartItemId}`);

    return fetch(`${API}/cart/${cartItemId}`, {
        method: 'DELETE',
        headers: getHeaders(true),
    })
        .then(handleResponse)
        .then(result => {
            console.log(' Removed from cart:', result);
            return result.data || result;
        });
};


export const createOrder = () => {
    console.log('📋 Creating order:', `${API}/order`);

    return fetch(`${API}/order`, {
        method: 'POST',
        headers: getHeaders(true),
    })
        .then(handleResponse)
        .then(result => {
            console.log(' Order created:', result);

            if (result.data) {
                return result.data;
            }
            return result;
        });
};

export const getOrders = () => {
    console.log(' Fetching orders from:', `${API}/order`);

    return fetch(`${API}/order`, {
        method: 'GET',
        headers: getHeaders(true),
    })
        .then(handleResponse)
        .then(result => {
            console.log(' Orders fetched:', result);

            const ordersData = result.data || [];

            return ordersData.map(order => ({
                id: order.id,
                products: order.products || [],
                order_price: order.order_price || 0,
                status: order.status || 'new',
                created_at: order.created_at || new Date().toISOString()
            }));
        });
};


export const logoutRequest = () => {
    console.log('🚪 Logout request to:', `${API}/logout`);

    return fetch(`${API}/logout`, {
        method: 'GET',
        headers: getHeaders(true),
    })
        .then(handleResponse)
        .then(result => {
            console.log(' Logout success:', result);
            return result.data || result;
        });
};


export const isAuthenticated = () => {
    return !!localStorage.getItem('myAppToken');
};

export const setToken = (token) => {
    if (token) {
        localStorage.setItem('myAppToken', token);
    } else {
        localStorage.removeItem('myAppToken');
    }
};


export const getToken = () => {
    return localStorage.getItem('myAppToken');
};


export const removeToken = () => {
    localStorage.removeItem('myAppToken');
};

