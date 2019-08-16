<template>
    <v-app id="app">
        <v-app-bar app clipped-left color="amber">
            <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
            <span class="title">校园&nbsp;<span class="font-weight-light">问答</span></span>
            <v-spacer></v-spacer>
            <!--            <v-text-field solo-inverted flat hide-details label="Search" color="amber darken-3"-->
            <!--                          prepend-inner-icon="mdi-comment-search-outline"></v-text-field>-->
            <v-autocomplete
                    style="margin-top: 2rem"
                    :items="searchItems" :loading="isLoading" :search-input.sync="search"
                    color="amber" dark solo clearable hide-no-data item-text="Content"
                    item-value="Content" placeholder="搜索" prepend-inner-icon="mdi-comment-search-outline"
                    return-object
            ></v-autocomplete>
        </v-app-bar>
        <v-navigation-drawer v-model="drawer" app clipped color="grey lighten-4">
            <v-list nav dense class="grey lighten-4">
                <div>
                    <v-list-item two-line>
                        <v-list-item-avatar>
                            <img :src="imgpath.public.userPic">
                        </v-list-item-avatar>
                        <v-list-item-content>
                            <v-list-item-title v-if="!isLogin">未登录</v-list-item-title>
                            <v-list-item-title v-else>{{userInfo.name}}</v-list-item-title>
                            <v-list-item-subtitle v-if="!isLogin">请先登录</v-list-item-subtitle>
                            <v-list-item-subtitle v-else>{{userInfo.college}}</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>
                    <div class="no-login" v-show="!isLogin">
                        <Login/>
                        <Register/>
                    </div>
                    <div class="is-login" v-show="isLogin">
                        <v-list-item color="amber" link>
                            <v-list-item-action>
                                <v-icon>mdi-account-circle</v-icon>
                            </v-list-item-action>
                            <v-list-item-content>
                                <v-list-item-title class="grey--text">
                                    个人中心
                                </v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                        <v-list-item color="amber" link @click="logOut">
                            <v-list-item-action>
                                <v-icon>mdi-logout</v-icon>
                            </v-list-item-action>
                            <v-list-item-content>
                                <v-list-item-title class="grey--text">
                                    注销
                                </v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </div>

                </div>
                <template v-for="(item, i) in navItems">
                    <v-layout v-if="item.heading" :key="i" align-center>
                        <v-flex xs6>
                            <v-subheader v-if="item.heading">
                                {{ item.heading }}
                            </v-subheader>
                        </v-flex>
                    </v-layout>
                    <v-divider v-else-if="item.divider" :key="i" dark class="my-4"></v-divider>
                    <v-list-item color="amber" v-else :key="i" link :to="item.to">
                        <v-list-item-action>
                            <v-icon>{{ item.icon }}</v-icon>
                        </v-list-item-action>
                        <v-list-item-content>
                            <v-list-item-title class="grey--text">
                                {{ item.text }}
                            </v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </template>
            </v-list>
        </v-navigation-drawer>

        <v-content>
            <v-container>
                <router-view/>
            </v-container>
        </v-content>
    </v-app>
</template>

<script>
    import axios from 'axios'
    import {Logout, QuestionsList, UserInfo} from "./assets/js/url";

    const Login = () => import('./components/Login');
    const Register = () => import('./components/Register');

    export default {
        components: {
            Login, Register
        },
        props: {
            source: String,
        },
        mounted() {
            let _this = this;
            // 实时获取登录态
            this.isLoginWatcher();
            clearInterval(this.timer);
            this.timer = window.setInterval(function () {
                _this.isLoginWatcher();
            }, 1000);
            // 获取状态信息
            if (sessionStorage.getItem("store")) {
                this.$store.replaceState(
                    Object.assign({},
                        this.$store.state,
                        JSON.parse(sessionStorage.getItem("store"))
                    )
                );
                sessionStorage.removeItem("store")
            }
            //在页面刷新时将vuex里的信息保存到sessionStorage里
            window.addEventListener("beforeunload", () => {
                sessionStorage.setItem("store", JSON.stringify(this.$store.state));
            });
            // 重新获取用户信息
            let userID = this.$store.state.currentUserID;
            if (userID !== '') {
                this.getUserInfo(userID);
            }
        },
        destroyed() {
            clearInterval(this.timer);
        },
        data: () => ({
            drawer: null,
            navItems: [
                {divider: true},
                {heading: '网站导航'},
                {icon: 'mdi-home', text: '知识广场', to: '/'},
                {icon: 'mdi-comment-question', text: '我要提问', to: '/askquestion'},
            ],
            contentLimit: 60,
            entries: [],
            timer: '',
            userInfo: [],
            isLogin: false,
            isLoading: false,
            search: null
        }),
        methods: {
            isLoginWatcher() {
                this.isLogin = this.$store.state.currentUserID !== ""
            },
            logOut() {
                axios.get(Logout).then(
                    res => {
                        if (res.data.status === 200) {
                            this.$store.commit("userChange", '');
                            this.isLoginWatcher();
                            this.userInfo = [];
                        }
                    }
                )
            },
            getUserInfo(userID) {
                axios.get(UserInfo + userID)
                    .then(
                        res => {
                            if (res.data.status === 200) {
                                this.userInfo = res.data.data[0];
                            }
                        }
                    )
            }
        },
        computed: {
            imgpath() {
                return this.$store.state.imageStyle;
            },
            currentUserID() {
                return this.$store.state.currentUserID;
            },
            searchItems() {
                return this.entries.map(entry => {
                    const Content = entry.Content.length > this.contentLimit
                        ? entry.Content.slice(0, this.contentLimit) + '...'
                        : entry.Content;
                    return Object.assign({}, entry, {Content})
                })
            },
            praseHTMLText(html) {
                return html.replace(/<[^>]*>|/g, "");
            }
        },
        watch: {
            currentUserID(userID) {
                if (userID !== "") {
                    this.getUserInfo(userID);
                }
            },
            search(val) {
                if (this.searchItems.length > 0) return;
                if (this.isLoading) return;
                this.isLoading = true;
                axios.get(QuestionsList)
                    .then(res => {
                        if (res.data.status === 200) {
                            let data = res.data.data;
                            console.log(data);
                            let count = data.length;
                            let entries = [];
                            for (let i in data) {
                                let content = data[i].title + ' ' + data[i].content.replace(/<[^>]*>|/g, "");
                                entries.push({
                                    QuestionID: data[i].pk,
                                    Content: content
                                })
                            }
                            this.count = count;
                            this.entries = entries
                        }
                    })
                    .catch(err => {
                        console.log(err)
                    })
                    .finally(() => (this.isLoading = false))
            }
        },
    }
</script>

<style>
    .title {
        width: 120px !important;
    }

    #keep .v-navigation-drawer__border {
        display: none
    }
</style>
