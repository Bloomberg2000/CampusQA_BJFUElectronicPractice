<template>
    <div class="questiondetail">
        <v-card id="create">
            <v-container fluid>
                <v-list-item>
                    <v-list-item-content>
                        <!--          <div class="overline mb-4">OVERLINE</div>-->
                        <v-list-item-title class="headline mb-1">{{questionInfo.title}}</v-list-item-title>
                        <v-list-item-subtitle><p>{{formatDate(questionInfo.createTime)}}</p></v-list-item-subtitle>
                        <v-list-item-content>
                            {{questionInfo.content}}
                        </v-list-item-content>
                    </v-list-item-content>
                </v-list-item>
            </v-container>
            <v-speed-dial v-model="fab" right bottom direction="left" transition="slide-x-reverse-transition">
                <template v-slot:activator>
                    <v-btn v-model="fab" color="amber" dark fab>
                        <v-icon v-if="fab">mdi-close</v-icon>
                        <v-icon v-else>mdi-toolbox</v-icon>
                    </v-btn>
                </template>
                <v-btn fab dark small color="green">
                    <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn fab dark small color="indigo">
                    <v-icon>mdi-plus</v-icon>
                </v-btn>
                <v-btn fab dark small color="red">
                    <v-icon>mdi-delete</v-icon>
                </v-btn>
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
                            <v-list-item-subtitle>{{formatDate(item.editTime)}}</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                    {{item.content}}
                </v-expansion-panel-content>
            </v-expansion-panel>
        </v-expansion-panels>
    </div>
</template>
<script>
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
                                this.questionInfo = res.data.data[0].fields;
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
            }
        },
        computed: {
            imgpath() {
                return this.$store.state.imageStyle
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
