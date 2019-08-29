<template>
    <v-app id="app">
        <v-app-bar app clipped-left color="amber">
            <v-app-bar-nav-icon @click="navDrawerShow = !navDrawerShow"></v-app-bar-nav-icon>
            <img style="height: 35px;" :src="imgpath.public.logo">
            <!--            <span class="title">校园&nbsp;<span class="font-weight-light">问答</span></span>-->
            <v-spacer/>
            <v-btn color="#616161" dark fab small @click.stop="drawer = !drawer">
                <v-icon>mdi-comment-search-outline</v-icon>
            </v-btn>
        </v-app-bar>
        <v-navigation-drawer v-model="drawer" absolute temporary right width="400">
            <v-list-item>
                <v-list-item-content>
                    <v-text-field color="amber" v-model="searchContent" label="搜索" placeholder="请输入搜索内容"></v-text-field>
                </v-list-item-content>
            </v-list-item>
            <v-divider></v-divider>
            <v-list dense>
                <div v-if="askNow">
                    <small style="padding: 10px">得知快问</small>
                    <v-list-item v-for="(item,index) in askNowResult" :key="index">
                        <v-list-item-content>
                            <span style="font-size: 20px;padding:5px 0px 5px 0px">{{item.fields.answer}}</span>
                            <v-list-item-subtitle style="padding:5px 0px 5px 0px">{{item.fields.question}}</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>
                    <v-divider></v-divider>
                </div>
                <div>
                    <small style="padding: 10px">搜索结果</small>
                    <v-list-item v-for="(item,index) in searchResult" :key="index"
                                 @click="questionDetail(item.questionID)">
                        <v-list-item-content>
                            <v-list-item-title style="font-size: 16px;">{{item.title}}</v-list-item-title>
                            <v-list-item-subtitle>{{praseHTMLText(item.content)}}</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>
                </div>
            </v-list>
        </v-navigation-drawer>
        <v-navigation-drawer v-model="navDrawerShow" app clipped color="grey lighten-4">
            <v-list nav dense class="grey lighten-4">
                <v-list-item two-line>
                    <v-list-item-avatar>
                        <img :src="imgpath.public.userPic">
                    </v-list-item-avatar>
                    <v-list-item-content>
                        <v-list-item-title>{{isLogin? userInfo.name: "未登录"}}</v-list-item-title>
                        <v-list-item-subtitle>{{isLogin? userInfo.college: "请先登录"}}</v-list-item-subtitle>
                    </v-list-item-content>
                </v-list-item>
                <div class="no-login" v-show="!isLogin">
                    <Login/>
                    <Register/>
                </div>
                <div class="is-login" v-show="isLogin">
                    <v-list-item color="amber" link @click="toPersonalCenter">
                        <v-list-item-action>
                            <v-icon>mdi-account-circle</v-icon>
                        </v-list-item-action>
                        <v-list-item-content>
                            <v-list-item-title class="grey--text">
                                个人中心
                            </v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                    <v-list-item color="amber" link @click="beforeLogOut">
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
        <v-dialog v-model="askDialogShow" persistent max-width="290">
            <v-card>
                <v-card-title class="headline">{{askDialogTitle}}</v-card-title>
                <v-card-text>{{askDialogMessage}}</v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="gray darken-3" text @click="askDialogShow = false">
                        取消
                    </v-btn>
                    <v-btn color="amber darken-3" text @click="askDialogAction">
                        确认
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-app>
</template>

<script>
    import axios from 'axios'
    import {Logout, SearchLink, UserInfo} from "./assets/js/url";

    const Login = () => import('./components/Login');
    const Register = () => import('./components/Register');

    export default {
        props: {
            source: String,
        },
        components: {
            Login, Register
        },
        data: () => ({
            drawer: false,
            items: [
                {title: 'Home', icon: 'dashboard'},
                {title: 'About', icon: 'question_answer'},
            ],
            navDrawerShow: null,
            navItems: [
                {divider: true},
                {heading: '网站导航'},
                {icon: 'mdi-home', text: '知识广场', to: '/'},
                {icon: 'mdi-comment-question', text: '我要提问', to: '/askquestion'},
            ],
            contentLimit: 60,
            userInfo: [],
            isLogin: false,
            timer: '',
            askDialogShow: false,
            askDialogTitle: '',
            askDialogMessage: '',
            askDialogToDo: '',
            searchContent: '',
            searchResult: [],
            askNow: false,
            askNowResult: [],
        }),
        destroyed() {
            clearInterval(this.timer);
        },
        mounted() {
            let _this = this;
            // 实时获取登录态
            this.isLoginWatcher();
            clearInterval(this.timer);
            this.timer = window.setInterval(function () {
                _this.isLoginWatcher();
            }, 100);
            // 每次打开页面重新获取用户信息
            let userID = this.$store.state.currentUserID;
            if (userID !== '') {
                this.getUserInfo(userID);
            }
        },
        methods: {
            toPersonalCenter() {
                this.$router.push({
                        path: "/personalcenter",
                        query: {
                            userID: this.currentUserID
                        }
                    }
                )
            },
            beforeLogOut() {
                this.askDialogShow = true;
                this.askDialogTitle = "注销";
                this.askDialogMessage = "您确定要注销吗";
                this.askDialogToDo = "logOut";
            },
            isLoginWatcher() {
                this.isLogin = this.$store.state.currentUserID !== ""
            },
            questionDetail(questionID) {
                this.$router.push({
                    path: "/questiondetail",
                    query: {
                        questionID: questionID
                    }
                });
            },
            askDialogAction() {
                if (this.askDialogToDo === "logOut") {
                    this.askDialogShow = false;
                    axios.get(Logout)
                        .then(
                            res => {
                                if (res.data.status === 200) {
                                    this.$store.commit("userChange", '');
                                    this.userInfo = [];
                                    this.isLoginWatcher();
                                }
                            }
                        )
                } else {
                    this.askDialogShow = false;
                }
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
            },
            doSearch(searchContent) {
                axios.get(SearchLink, {
                    params: {
                        keyword: searchContent
                    }
                })
                    .then(
                        res => {
                            this.askNow = false;
                            this.askNowResult = '';
                            this.searchResult = [];
                            if (res.data.status === 200) {
                                if (res.data.data.askNow.length > 0) {
                                    this.askNow = true;
                                    this.askNowResult = res.data.data.askNow;
                                }
                                this.searchResult = res.data.data.searchResult;
                            }
                        }
                    )
            },
            praseHTMLText(html) {
                return html.replace(/<[^>]*>|/g, "");
            },
        },
        computed: {
            imgpath() {
                return this.$store.state.imageStyle;
            },
            currentUserID() {
                return this.$store.state.currentUserID;
            }
        },
        watch: {
            currentUserID(userID) {
                // 用户ID变化重新获取用户信息
                if (userID !== "") {
                    this.getUserInfo(userID);
                }
            },
            searchContent(val) {
                this.doSearch(val);
            }
        }
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
