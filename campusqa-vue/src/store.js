import Vue from 'vue'
import Vuex from 'vuex'
import imagePath from '@/assets/js/image.js'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        imageStyle: imagePath,
    },
    mutations: {},
    actions: {}
})
