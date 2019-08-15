<template>
    <div class="home" style="margin-top: 15px">
        <div class="list" v-for="(item,index) in questionsList" v-bind:key="index">
            <v-hover v-slot:default="{ hover }">
                <v-card :elevation="hover ? 12 : 2" outlined class="mx-auto"
                        style="margin-top: 10px;margin-bottom: 15px" @click="questionDetail(item.pk)">
                    <v-list-item three-line>
                        <v-list-item-content>
                            <!--          <div class="overline mb-4">OVERLINE</div>-->
                            <v-list-item-title class="headline mb-1">{{item.fields.title}}</v-list-item-title>
                            <v-list-item-subtitle>{{praseHTMLText(item.fields.content)}}</v-list-item-subtitle>
                        </v-list-item-content>
                        <v-list-item-avatar tile size="80">
                            <!--                            <img :src="item.fields.picture">-->
                        </v-list-item-avatar>
                    </v-list-item>
                    <v-card-actions style="margin-right: 10px">
                        <v-spacer></v-spacer>
                        <v-btn outlined @click="questionDetail(item.pk)">查看问题</v-btn>

                        <!--                <v-btn icon>-->
                        <!--                    <v-icon>mdi-heart</v-icon>-->
                        <!--                </v-btn>-->
                    </v-card-actions>
                </v-card>
            </v-hover>
            <v-spacer></v-spacer>
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
