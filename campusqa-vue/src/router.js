import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'home',
            component: () => import(/* webpackChunkName: "about" */ './views/Home.vue')
        },
        {
            path: '/askquestion',
            name: 'askquestion',
            component: () => import(/* webpackChunkName: "about" */ './views/AskQuestion.vue')
        },
        {
            path: '/questiondetail',
            name: 'questiondetail',
            // route level code-splitting
            // this generates a separate chunk (about.[hash].js) for this route
            // which is lazy-loaded when the route is visited.
            component: () => import(/* webpackChunkName: "about" */ './views/QuestionDetail.vue')
        }
    ]
})
