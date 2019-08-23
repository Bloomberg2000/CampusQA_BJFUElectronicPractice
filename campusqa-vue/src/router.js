import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'home',
            component: () => import(/* webpackChunkName: "about" */ './views/Home.vue'),
            meta: {title: '知识广场-得知'},
        },
        {
            path: '/askquestion',
            name: 'askquestion',
            component: () => import(/* webpackChunkName: "about" */ './views/AskQuestion.vue'),
            meta: {title: '我要提问-得知'},
        },
        {
            path: '/questiondetail',
            name: 'questiondetail',
            component: () => import(/* webpackChunkName: "about" */ './views/QuestionDetail.vue'),
            meta: {title: '问题详情-得知'},
        },
        {
            path: '/personalcenter',
            name: 'personalcenter',
            component: () => import(/* webpackChunkName: "about" */ './views/PersonalCenter.vue'),
            meta: {title: '问题详情-得知'},
        }
    ]
})
