<template>
    <div class="questiondetail">
        <v-card id="create">
            <v-container fluid>
                <v-list-item>
                    <v-list-item-content>
                        <!--          <div class="overline mb-4">OVERLINE</div>-->
                        <v-list-item-title class="headline mb-1">{{questionInfo.title}}</v-list-item-title>
                        <v-list-item-subtitle><p>{{formatDate(questionInfo.createTime)}}</p></v-list-item-subtitle>
                        <v-list-item-content v-html="questionInfo.content">
                        </v-list-item-content>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item>
                    <v-list-item-avatar>
                        <img :src="imgpath.public.userPic">
                    </v-list-item-avatar>
                    <v-list-item-content>
                        <v-list-item-title>{{questionInfo.createUser.name}}</v-list-item-title>
                        <v-list-item-subtitle>{{questionInfo.editTime}}</v-list-item-subtitle>
                    </v-list-item-content>
                </v-list-item>
            </v-container>
            <v-speed-dial v-model="fab" right bottom direction="left" transition="slide-x-reverse-transition">
                <template v-slot:activator>
                    <v-tooltip bottom>
                        <template v-slot:activator="{ on }">
                            <v-btn v-model="fab" color="amber" dark fab v-on="on">
                                <v-icon v-if="fab">mdi-close</v-icon>
                                <v-icon v-else>mdi-toolbox</v-icon>
                            </v-btn>
                        </template>
                        <span v-if="fab">关闭</span>
                        <span v-else>工具箱</span>
                    </v-tooltip>
                </template>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on }">
                        <v-btn fab dark small color="indigo" v-on="on">
                            <v-icon>mdi-plus</v-icon>
                        </v-btn>
                    </template>
                    <span>添加回答</span>
                </v-tooltip>
                <v-tooltip v-if="authorityJudgment(questionInfo.createUser.userID)" bottom>
                    <template v-slot:activator="{ on }">
                        <v-btn fab dark small color="green" v-on="on">
                            <v-icon>mdi-pencil</v-icon>
                        </v-btn>
                    </template>
                    <span>编辑问题</span>
                </v-tooltip>
                <v-tooltip v-if="authorityJudgment(questionInfo.createUser.userID)" bottom>
                    <template v-slot:activator="{ on }">
                        <v-btn fab dark small color="red" v-on="on">
                            <v-icon>mdi-delete</v-icon>
                        </v-btn>
                    </template>
                    <span>删除问题</span>
                </v-tooltip>
            </v-speed-dial>
        </v-card>
        <v-expansion-panels popout multiple style="margin-top: 20px">
            <v-expansion-panel v-for="(item,index) in answerList" :key="index">
                <v-expansion-panel-header>
                    <v-list-item>
                        <v-list-item-avatar>
                            <img :src="imgpath.public.userPic">
                        </v-list-item-avatar>
                        <v-list-item-content>
                            <v-list-item-title>{{item.createUser.name}}</v-list-item-title>
                            <v-list-item-subtitle>{{item.editTime}}</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                    {{item.content}}
                    <v-card-actions style="margin-top: 1rem; margin-bottom: -0.5rem">
                        <v-tooltip v-if="authorityJudgment(item.createUser.userID)" bottom>
                            <template v-slot:activator="{ on }">
                                <v-btn text fab dark small color="grey darken-1" v-on="on">
                                    <v-icon>mdi-pencil</v-icon>
                                </v-btn>
                            </template>
                            <span>编辑回答</span>
                        </v-tooltip>
                        <v-tooltip v-if="authorityJudgment(item.createUser.userID)" bottom>
                            <template v-slot:activator="{ on }">
                                <v-btn text fab dark small color="grey darken-1" v-on="on">
                                    <v-icon>mdi-delete</v-icon>
                                </v-btn>
                            </template>
                            <span>删除回答</span>
                        </v-tooltip>
                        <v-spacer></v-spacer>
                        <v-tooltip bottom>
                            <template v-slot:activator="{ on }">
                                <v-btn text fab dark small color="grey darken-1" v-on="on">
                                    <v-icon>mdi-heart</v-icon>
                                </v-btn>
                            </template>
                            <span>喜欢</span>
                        </v-tooltip>
                    </v-card-actions>
                </v-expansion-panel-content>
            </v-expansion-panel>
        </v-expansion-panels>
    </div>
</template>
<script>
    import 'quill/dist/quill.core.css';
    import 'quill/dist/quill.snow.css';
    import 'quill/dist/quill.bubble.css';
    import axios from 'axios'
    import {AnswersInfo, QuestionsInfo} from "../assets/js/url";

    export default {
        data: () => ({
            questionID: 0,
            questionInfo: [],
            answerList: [],
            fab: false
        }),
        mounted() {
            this.questionID = this.$route.query.questionID;
            console.log(this.$route.query.questionID);
            this.getQuestionInfo();
            this.getAnswers();
        },
        methods: {
            getQuestionInfo() {
                axios.get(QuestionsInfo + this.questionID)
                    .then(
                        res => {
                            if (res.data.status === 200) {
                                this.questionInfo = res.data.data[0];
                                console.log(this.questionInfo)
                            }
                        }
                    )
            },
            getAnswers() {
                axios.get(AnswersInfo + this.questionID)
                    .then(
                        res => {
                            if (res.data.status === 200) {
                                this.answerList = res.data.data;
                            }
                        }
                    )
            },
            formatDate(inputTime) {
                if (!inputTime && typeof inputTime !== 'number') {
                    return '';
                }
                var localTime = '';
                inputTime = new Date(inputTime).getTime();
                const offset = (new Date()).getTimezoneOffset();
                localTime = (new Date(inputTime - offset * 60000)).toISOString();
                localTime = localTime.substr(0, localTime.lastIndexOf('.'));
                localTime = localTime.replace('T', ' ');
                return localTime;
            },
            authorityJudgment(accessUserID) {
                return accessUserID + '' === this.currentUserID;
            }
        },
        computed: {
            imgpath() {
                return this.$store.state.imageStyle
            },
            currentUserID() {
                return this.$store.state.currentUserID;
            }
        },
        watch: {
            top(val) {
                this.bottom = !val
            }
            ,
            right(val) {
                this.left = !val
            }
            ,
            bottom(val) {
                this.top = !val
            }
            ,
            left(val) {
                this.right = !val
            }
            ,
        }
        ,
    }
</script>
<style>
    /* This is for documentation purposes and will not be needed in your application */
    #create .v-speed-dial {
        position: absolute;
    }

    #create .v-btn--floating {
        position: relative;
    }
</style>
