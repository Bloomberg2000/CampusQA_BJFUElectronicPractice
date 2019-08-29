import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import router from './router'
import store from './store'
import vueiInfinite from 'vue-infinite-scroll'

Vue.use(vueiInfinite);

new Vue({
    vuetify,
    router,
    store,
    render: h => h(App)
}).$mount('#app')

Vue.config.productionTip = false

router.beforeEach((to, from, next) => {
    /* 路由发生变化修改页面title */
    if (to.meta.title) {
        document.title = to.meta.title
    }
    next()
})
