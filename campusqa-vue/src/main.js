import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import router from './router'

// require styles
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'
import VueQuillEditor from 'vue-quill-editor'


new Vue({
  // vuetify,
  router,
  render: h => h(App)
}).$mount('#app')

Vue.use(VueQuillEditor)
Vue.use(vuetify)

Vue.config.productionTip = false
