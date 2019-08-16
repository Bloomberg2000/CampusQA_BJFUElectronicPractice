<template>
    <div class="questiondetail">
        <v-card id="create">
            <v-container fluid>
                <v-list-item>
                    <v-list-item-content>
                        <!--          <div class="overline mb-4">OVERLINE</div>-->
                        <v-list-item-title class="headline mb-1">{{questionInfo.title}}</v-list-item-title>
                        <v-list-item-subtitle><p>{{questionInfo.createTime}}</p></v-list-item-subtitle>
                        <v-list-item-content v-html="questionInfo.content">
                        </v-list-item-content>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item>
                    <v-list-item-avatar>
                        <img :src="imgpath.public.userPic">
                    </v-list-item-avatar>
                    <v-list-item-content>
                        <v-list-item-title>{{questionInfo.createUserName}}</v-list-item-title>
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
                        <v-btn fab dark small color="indigo" v-on="on" @click="expand = true">
                            <v-icon>mdi-plus</v-icon>
                        </v-btn>
                    </template>
                    <span>添加回答</span>
                </v-tooltip>
                <v-tooltip v-if="authorityJudgment(questionInfo.createUserID)" bottom>
                    <template v-slot:activator="{ on }">
                        <v-btn fab dark small color="green" v-on="on">
                            <v-icon>mdi-pencil</v-icon>
                        </v-btn>
                    </template>
                    <span>编辑问题</span>
                </v-tooltip>
                <v-tooltip v-if="authorityJudgment(questionInfo.createUserID)" bottom>
                    <template v-slot:activator="{ on }">
                        <v-btn fab dark small color="red" v-on="on" @click="deleteQuestion">
                            <v-icon>mdi-delete</v-icon>
                        </v-btn>
                    </template>
                    <span>删除问题</span>
                </v-tooltip>
            </v-speed-dial>
        </v-card>
        <v-expand-transition>
            <v-card v-show="expand" class="mx-auto" style="margin-top: 1rem">
                <v-card-title>
                    <span class="headline">创建回答</span>
                </v-card-title>
                <v-card-text>
                    <v-container grid-list-md>
                        <v-form ref="form">
                            <v-layout wrap>
                                <v-flex xs12>
                                    <small style="position:absolute;margin-left:13px;margin-top: -10px;background-color: #ffffff">
                                        回答内容*
                                    </small>
                                    <quill-editor ref="myQuillEditor" :options="editorOption"
                                                  v-model="AnswerForm.content"></quill-editor>

                                </v-flex>
                            </v-layout>
                        </v-form>
                    </v-container>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="amber darken-3" text @click="expand = false">取消</v-btn>
                    <v-btn text color="amber darken-3" @click="answerQuestion">发布回答</v-btn>
                </v-card-actions>
            </v-card>
        </v-expand-transition>
        <v-expansion-panels popout multiple style="margin-top: 20px">
            <v-expansion-panel v-for="(item,index) in answerList" :key="index">
                <v-expansion-panel-header>
                    <v-list-item>
                        <v-list-item-avatar>
                            <img :src="imgpath.public.userPic">
                        </v-list-item-avatar>
                        <v-list-item-content>
                            <v-list-item-title>{{item.createUserName}}</v-list-item-title>
                            <v-list-item-subtitle>{{item.editTime}}</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                    <div v-html="item.content"></div>
                    <v-card-actions style="margin-top: 1rem; margin-bottom: -0.5rem">
                        <v-tooltip v-if="authorityJudgment(item.createUserID)" bottom>
                            <template v-slot:activator="{ on }">
                                <v-btn text fab dark small color="grey darken-1" v-on="on" :disabled="!answerEditing">
                                    <v-icon>mdi-pencil</v-icon>
                                </v-btn>
                            </template>
                            <span>编辑回答</span>
                        </v-tooltip>
                        <v-tooltip v-if="authorityJudgment(item.createUserID)" bottom>
                            <template v-slot:activator="{ on }">
                                <v-btn text fab dark small color="grey darken-1" v-on="on" @click="deleteAnswer(item.answerID)">
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
        <v-dialog v-model="dialog" persistent max-width="290">
            <v-card>
                <v-card-title class="headline">{{dialogTitle}}</v-card-title>
                <v-card-text>{{dialogMessage}}</v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="amber darken-3" text @click="dialogBackToHome?backToHome():dialog = false">好的</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-snackbar v-model="snackBar">
            {{ snackBarMessage }}
            <v-btn color="amber" text @click="snackBar = false">
                关闭
            </v-btn>
        </v-snackbar>
    </div>
</template>
<script>
    import 'quill/dist/quill.core.css';
    import 'quill/dist/quill.snow.css';
    import 'quill/dist/quill.bubble.css';
    import {quillEditor} from "vue-quill-editor"; //调用编辑器
    import axios from 'axios'
    import {AnswerQuestion, AnswersInfo, DeleteAnswer, DeleteQuestion, QuestionsInfo} from "../assets/js/url";

    export default {
        components: {
            quillEditor
        },
        data: () => ({
            questionID: 0,
            questionInfo: [],
            answerList: [],
            AnswerForm: {
                content: ''
            },
            answerEditing: true,
            QuestionEditForm: {
                title: '',
                content: ''
            },
            AnswerEditForm: {
                content: ''
            },
            fab: false,
            expand: false,
            dialog: false,
            dialogTitle: '',
            dialogMessage: '',
            dialogBackToHome: false,
            snackBar:false,
            snackBarMessage:'',
            editorOption: {
                modules: {
                    toolbar: [
                        ['bold', 'italic', 'underline', 'strike'],
                        ['blockquote'],
                        [{'header': 1}, {'header': 2}],
                        [{'list': 'ordered'}, {'list': 'bullet'}],
                        [{'script': 'sub'}, {'script': 'super'}],
                        [{'indent': '-1'}, {'indent': '+1'}],
                        [{'size': [false, 'large', 'huge']}],
                        [{'header': [1, 2, 3, 4, 5, 6, false]}],
                        [{'align': []}],
                        ['link', 'image']
                    ]
                },
                placeholder: '请输入回答内容'
            }
        }),
        mounted() {
            this.questionID = this.$route.query.questionID;
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
            authorityJudgment(accessUserID) {
                return accessUserID + '' === this.currentUserID;
            },
            deleteQuestion() {
                axios.get(DeleteQuestion + this.questionID)
                    .then(
                        res => {
                            if (res.data.status === 200) {
                                this.dialog = true;
                                this.dialogTitle = "删除成功";
                                this.dialogMessage = "下面将为您跳转到首页";
                                this.dialogBackToHome = true;
                            }
                        }
                    )
            },
            deleteAnswer(answerID) {
                axios.get(DeleteAnswer + answerID)
                    .then(
                        res => {
                            if (res.data.status === 200) {
                                this.snackBar = true;
                                this.snackBarMessage = "回答删除成功！";
                                this.getAnswers();
                            } else {
                                this.dialog = true;
                                this.dialogTitle = "删除失败";
                                this.dialogMessage = res.data.message;
                                this.dialogBackToHome = false;
                            }
                        }
                    )
            },
            answerQuestion() {
                let formData = new FormData();
                formData.append('content', this.AnswerForm.content);
                axios.post(AnswerQuestion + this.questionID, formData).then(
                    res => {
                        if (res.data.status === 200) {
                            this.snackBar = true;
                            this.snackBarMessage = "回答发布成功！";
                            this.AnswerForm.content = '';
                            this.expand = false
                            this.getAnswers();
                        } else {
                            this.dialog = true;
                            this.dialogTitle = "发布失败";
                            this.dialogMessage = res.data.message;
                            this.dialogBackToHome = false;
                        }
                    }
                )
            },
            backToHome() {
                this.dialogBackToHome = false;
                this.$router.push({
                    path: "/",
                });
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
            },
            right(val) {
                this.left = !val
            },
            bottom(val) {
                this.top = !val
            },
            left(val) {
                this.right = !val
            }
        }
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

    .ql-toolbar.ql-snow {
        border-radius: 4px 4px 0 0;
    }

    .ql-container.ql-snow {
        border-radius: 0 0 4px 4px;
    }

    .ql-editor.ql-blank::before {
        font-style: normal;
        color: rgba(0, 0, 0, 0.5);
        font-size: 15px;
    }

</style>
