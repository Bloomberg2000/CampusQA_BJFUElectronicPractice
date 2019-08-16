<template>
    <div class="home" style="margin-top: 15px">
        <div class="list" v-for="(item,index) in questionsList" v-bind:key="index">
            <v-hover v-slot:default="{ hover }">
                <v-card :elevation="hover ? 12 : 0" outlined class="mx-auto"
                        @click="questionDetail(item.questionID)" style="margin-top: 10px;margin-bottom: 15px">
                    <v-list-item three-line style="margin-left: 0.5rem;">
                        <v-list-item-content>
                            <div class="overline mb-4">Q&A</div>
                            <v-list-item-title class="headline mb-1">{{item.title}}</v-list-item-title>
                            <v-list-item-subtitle>{{praseHTMLText(item.content)}}</v-list-item-subtitle>
                        </v-list-item-content>
                        <v-list-item-avatar tile size="80">
                            <!--                            <img :src="item.fields.picture">-->
                        </v-list-item-avatar>
                    </v-list-item>
                    <v-list-item two-line style="margin-bottom: 0.5rem; margin-top: 1rem; margin-left: 0.5rem">
                        <v-list-item-avatar>
                            <img :src="imgpath.public.userPic">
                        </v-list-item-avatar>
                        <v-list-item-content>
                            <v-list-item-title>{{item.createUserName}}</v-list-item-title>
                            <v-list-item-subtitle>{{item.editTime}}</v-list-item-subtitle>
                        </v-list-item-content>
                        <v-spacer/>
                        <v-card-actions style="margin-right: 10px">
                            <v-btn outlined @click="questionDetail(item.questionID)">查看问题</v-btn>
                        </v-card-actions>
                    </v-list-item>
                </v-card>
            </v-hover>
        </div>
    </div>
</template>
<script>
    import axios from 'axios'
    import {QuestionsList} from "../assets/js/url.js";

    export default {
        data: () => ({
            questionsList: []
        }),
        mounted() {
            this.getQuestionList();
        },
        methods: {
            getQuestionList() {
                axios.get(QuestionsList)
                    .then(
                        res => {
                            if (res.data.status === 200) {
                                this.questionsList = res.data.data;
                            }
                        }
                    )
            },
            questionDetail(questionID) {
                this.$router.push({
                    path: "/questiondetail",
                    query: {
                        questionID: questionID
                    }
                });
            },
            praseHTMLText(html) {
                // 富文本转换为纯文字
                return html.replace(/<[^>]*>|/g, "");
            }
        },
        computed: {
            imgpath() {
                return this.$store.state.imageStyle
            },
        }
    }
</script>
