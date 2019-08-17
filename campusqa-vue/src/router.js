import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'home',
            component: () => import(/* webpackChunkName: "about" */ './views/Home.vue'),
            meta: {title:'知识广场-校园问答'},
        },
        {
            path: '/askquestion',
            name: 'askquestion',
            component: () => import(/* webpackChunkName: "about" */ './views/AskQuestion.vue'),
            meta: {title:'我要提问-校园问答'},
        },
        {
            path: '/questiondetail',
            name: 'questiondetail',
            // route level code-splitting
            // this generates a separate chunk (about.[hash].js) for this route
            // which is lazy-loaded when the route is visited.
            component: () => import(/* webpackChunkName: "about" */ './views/QuestionDetail.vue'),
            meta: {title:'问题详情-校园问答'},
        }
    ]
})
