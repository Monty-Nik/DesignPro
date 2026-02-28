<template>
  <div id="app">
    <nav>
      <div class="nav-container">
        <router-link to="/" class="logo">My Shop</router-link>
        <div class="nav-links">
          <router-link to="/">Каталог</router-link>
          <router-link to="/cart" v-if="isAuthenticated">Корзина ({{ cartCount }})</router-link>
          <router-link to="/orders" v-if="isAuthenticated">Мои заказы</router-link>
          <router-link to="/login" v-if="!isAuthenticated">Вход</router-link>
          <router-link to="/register" v-if="!isAuthenticated">Регистрация</router-link>
          <a href="#" @click.prevent="logout" v-if="isAuthenticated">Выйти</a>
        </div>
      </div>
    </nav>

    <main>
      <router-view />
    </main>

    <div v-if="error" class="error-message">
      {{ error }}
      <button @click="clearError">×</button>
    </div>

    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const store = useStore()
    const router = useRouter()

    const isAuthenticated = computed(() => store.getters.isAuthenticated)
    const cartCount = computed(() => store.state.cart.length)
    const loading = computed(() => store.getters.loading)
    const error = computed(() => store.getters.error)

    const logout = () => {
      store.dispatch('logout')
      router.push('/')
    }

    const clearError = () => {
      store.commit('SET_ERROR', null)
    }

    return {
      isAuthenticated,
      cartCount,
      loading,
      error,
      logout,
      clearError
    }
  }
}
</script>

<style src="@/assets/styles/main.css"></style>