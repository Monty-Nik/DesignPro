import { createStore } from 'vuex';
import {
    loginRequest,
    registerRequest,
    getProducts,
    getCart,
    addToCart,
    removeFromCart,
    createOrder,
    getOrders,
    logoutRequest
} from '@/utils/api';

export default createStore({
    state: {
        token: localStorage.getItem('myAppToken') || '',
        user: null,
        products: [],
        cart: [],
        orders: [],
        loading: false,
        error: null
    },

    getters: {
        isAuthenticated: (state) => !!state.token,
        isGuest: (state) => !state.token,
        products: (state) => state.products,
        cart: (state) => state.cart,
        orders: (state) => state.orders,
        loading: (state) => state.loading,
        error: (state) => state.error
    },

    mutations: {
        AUTH_SUCCESS: (state, token) => {
            state.token = token;
            localStorage.setItem('myAppToken', token);
            state.error = null;
        },
        AUTH_ERROR: (state) => {
            state.token = '';
            localStorage.removeItem('myAppToken');
            state.user = null;
        },

        SET_USER: (state, user) => {
            state.user = user;
        },
        SET_PRODUCTS: (state, products) => {
            state.products = products;
        },
        SET_CART: (state, cart) => {
            state.cart = cart;
        },
        SET_ORDERS: (state, orders) => {
            state.orders = orders;
        },
        SET_LOADING: (state, loading) => {
            state.loading = loading;
        },
        SET_ERROR: (state, error) => {
            state.error = error;
        },
        CLEAR_ERROR: (state) => {
            state.error = null;
        }
    },

    actions: {
        AUTH_REQUEST: ({ commit }, credentials) => {
            commit('SET_LOADING', true);
            commit('CLEAR_ERROR');

            return new Promise((resolve, reject) => {
                loginRequest(credentials)
                    .then((token) => {
                        console.log('Login successful, token:', token);
                        commit('AUTH_SUCCESS', token);
                        resolve(token);
                    })
                    .catch((error) => {
                        console.error('Login error:', error);
                        commit('AUTH_ERROR');
                        commit('SET_ERROR', error.message || 'Ошибка авторизации');
                        reject(error);
                    })
                    .finally(() => {
                        commit('SET_LOADING', false);
                    });
            });
        },

        REGISTER_REQUEST: ({ commit }, userData) => {
            commit('SET_LOADING', true);
            commit('CLEAR_ERROR');

            return new Promise((resolve, reject) => {
                registerRequest(userData)
                    .then((token) => {
                        console.log('Registration successful, token:', token);
                        resolve(token);
                    })
                    .catch((error) => {
                        console.error('Registration error:', error);
                        commit('SET_ERROR', error.message || 'Ошибка регистрации');
                        reject(error);
                    })
                    .finally(() => {
                        commit('SET_LOADING', false);
                    });
            });
        },

        logout: ({ commit }) => {
            commit('SET_LOADING', true);

            return logoutRequest()
                .then(() => {
                    commit('AUTH_ERROR');
                    commit('SET_CART', []);
                    commit('SET_ORDERS', []);
                })
                .catch((error) => {
                    console.error('Logout error:', error);
                    commit('AUTH_ERROR');
                })
                .finally(() => {
                    commit('SET_LOADING', false);
                });
        },

        fetchProducts: ({ commit }) => {
            commit('SET_LOADING', true);

            return getProducts()
                .then((products) => {
                    commit('SET_PRODUCTS', products);
                })
                .catch((error) => {
                    console.error('Fetch products error:', error);
                    commit('SET_ERROR', error.message);
                })
                .finally(() => {
                    commit('SET_LOADING', false);
                });
        },

        fetchCart: ({ commit, state }) => {
            if (!state.token) return Promise.resolve();

            commit('SET_LOADING', true);

            return getCart()
                .then((cart) => {
                    commit('SET_CART', cart || []);
                })
                .catch((error) => {
                    console.error('Fetch cart error:', error);
                    commit('SET_ERROR', error.message);
                })
                .finally(() => {
                    commit('SET_LOADING', false);
                });
        },

        addToCart: ({ commit, dispatch }, productId) => {
            commit('SET_LOADING', true);

            return addToCart(productId)
                .then(() => {
                    return dispatch('fetchCart');
                })
                .catch((error) => {
                    console.error('Add to cart error:', error);
                    commit('SET_ERROR', error.message);
                    throw error;
                })
                .finally(() => {
                    commit('SET_LOADING', false);
                });
        },

        removeFromCart: ({ commit, dispatch }, cartItemId) => {
            commit('SET_LOADING', true);

            return removeFromCart(cartItemId)
                .then(() => {
                    return dispatch('fetchCart');
                })
                .catch((error) => {
                    console.error('Remove from cart error:', error);
                    commit('SET_ERROR', error.message);
                    throw error;
                })
                .finally(() => {
                    commit('SET_LOADING', false);
                });
        },

        checkout: ({ commit, dispatch }) => {
            commit('SET_LOADING', true);

            return createOrder()
                .then((result) => {
                    dispatch('fetchCart');
                    return result;
                })
                .catch((error) => {
                    console.error('Checkout error:', error);
                    commit('SET_ERROR', error.message);
                    throw error;
                })
                .finally(() => {
                    commit('SET_LOADING', false);
                });
        },

        fetchOrders: ({ commit, state }) => {
            if (!state.token) return Promise.resolve();

            commit('SET_LOADING', true);

            return getOrders()
                .then((orders) => {
                    commit('SET_ORDERS', orders || []);
                })
                .catch((error) => {
                    console.error('Fetch orders error:', error);
                    commit('SET_ERROR', error.message);
                })
                .finally(() => {
                    commit('SET_LOADING', false);
                });
        }
    }
});