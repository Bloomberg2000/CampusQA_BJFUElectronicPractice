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
                            <v-tooltip bottom>
                                <template v-slot:activator="{ on }">
                                    <v-btn text fab small color="grey darken-1" v-on="on"
                                           @click="questionDetail(item.questionID)">
                                        <v-icon>mdi-more</v-icon>
                                    </v-btn>
                                </template>
                                <span>查看问题</span>
                            </v-tooltip>
                        </v-card-actions>
                    </v-list-item>
                </v-card>
            </v-hover>
        </div>
        <div v-infinite-scroll="loadMore" infinite-scroll-disabled="busy" infinite-scroll-distance="5">
            <div style="text-align: center" v-if="hasMore">
                <v-chip class="ma-2" color="amber" outlined>
                    <v-icon style="margin-right: 3px" class="mdi-spin">mdi-loading</v-icon>
                    加载中
                </v-chip>
            </div>
            <div style="text-align: center" v-else>
                <v-chip class="ma-2" color="amber" outlined>
                    <v-icon style="margin-right: 3px">mdi-emoticon-excited</v-icon>
                    没有更多问题啦～
                </v-chip>
            </div>
        </div>
    </div>
</template>
<script>
    import axios from 'axios'
    import {QuestionsList} from "../assets/js/url.js";

    export default {
        data: () => ({
            busy: false,
            questionsList: [],
            hasMore: true,
            pageData: {
                totalPage: 0,
                dataCount: 0,
                currentPage: 1,
                pageSize: 10
            }
        }),
        mounted() {
            this.getQuestionList(this.pageData.pageSize, this.pageData.currentPage, false);
        },
        methods: {
            getQuestionList(pageSize, pageNum, append_flag) {
                axios.get(QuestionsList, {
                    params: {
                        pageSize: pageSize,
                        pageNum: pageNum
                    }
                })
                    .then(
                        res => {
                            if (res.data.status === 200) {
                                this.pageData.totalPage = res.data.data.totalPage;
                                this.pageData.dataCount = res.data.data.dataCount;
                                if (append_flag) {
                                    this.questionsList = this.questionsList.concat(res.data.data.data);
                                } else {
                                    this.questionsList = res.data.data.data;
                                    this.busy = false
                                }
                            }
                            if (res.data.status === 406) {
                                this.busy = true;
                                this.hasMore = false;
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
                return html.replace(/<[^>]*>|/g, "");
            },
            loadMore() {
                this.busy = true;
                //把busy置位true，这次请求结束前不再执行
                setTimeout(() => {
                    this.pageData.currentPage++;
                    this.getQuestionList(this.pageData.pageSize, this.pageData.currentPage, true);
                }, 1300)
            }
        },
        computed: {
            imgpath() {
                return this.$store.state.imageStyle
            },
        }
    }
</script>
<style>
    .v-list-item__title, .v-list-item__subtitle {
        white-space: normal;
    }
</style>
