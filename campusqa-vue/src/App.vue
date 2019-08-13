<template>
    <v-app id="app">
        <v-app-bar app clipped-left color="amber">
            <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
            <span class="title ml-3 mr-8">校园&nbsp;<span class="font-weight-light">问答平台</span></span>
            <v-spacer></v-spacer>
            <v-text-field solo-inverted flat hide-details label="Search"
                          prepend-inner-icon="mdi-comment-search-outline"></v-text-field>
        </v-app-bar>

        <v-navigation-drawer v-model="drawer" app clipped color="grey lighten-4">
            <v-list nav dense class="grey lighten-4">

                <v-list-item two-line>
                    <v-list-item-avatar>
                        <img src="@/assets/userpic.jpg">
                    </v-list-item-avatar>
                    <v-list-item-content>
                        <v-list-item-title>未登录</v-list-item-title>
                        <v-list-item-subtitle>请先登录</v-list-item-subtitle>
                    </v-list-item-content>
                </v-list-item>
                <Login/>
                <Register/>

                <template v-for="(item, i) in items">
                    <v-layout v-if="item.heading" :key="i" align-center>
                        <v-flex xs6>
                            <v-subheader v-if="item.heading">
                                {{ item.heading }}
                            </v-subheader>
                        </v-flex>
                    </v-layout>
                    <v-divider v-else-if="item.divider" :key="i" dark class="my-4"></v-divider>
                    <v-list-item v-else :key="i" link :to="item.to">
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
    import Login from "./components/Login";
    import Register from "./components/Register";

    export default {
        components: {Login, Register},
        props: {
            source: String,
        },
        data: () => ({
            drawer: null,
            items: [
                {divider: true},
                {heading: '网站导航'},
                {icon: 'mdi-home', text: '知识广场', to: '/'},
                {icon: 'mdi-comment-question', text: '我要提问', to: '/askquestion'},
            ],
        }),
    }
</script>

<style>
    #keep .v-navigation-drawer__border {
        display: none
    }
</style>
