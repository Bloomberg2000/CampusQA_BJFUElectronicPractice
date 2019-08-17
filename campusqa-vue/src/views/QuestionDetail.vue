<template>
    <div class="questiondetail">
        <!--        问题详情-->
        <v-expand-transition>
            <v-card id="create" v-if="!questionEdit">
                <v-container fluid>
                    <v-list-item>
                        <v-list-item-content>
                            <div class="overline mb-4">问题详情</div>
                            <v-list-item-title class="headline mb-1">
                                {{questionInfo.title}}
                            </v-list-item-title>
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
                            <v-list-item-subtitle>{{questionInfo.createTime}}</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>
                </v-container>
                <v-speed-dial v-model="floatButtonClicked" right bottom direction="left"
                              transition="slide-x-reverse-transition">
                    <template v-slot:activator>
                        <v-tooltip bottom>
                            <template v-slot:activator="{ on }">
                                <div>
                                    <v-btn class="ma-1" ref="fabButton" v-model="floatButtonClicked" color="amber" dark fab v-on="on">
                                        <v-icon v-if="floatButtonClicked">mdi-close</v-icon>
                                        <v-icon v-else>mdi-toolbox</v-icon>
                                    </v-btn>
                                </div>
                            </template>
                            <span v-if="floatButtonClicked">关闭</span>
                            <span v-else>工具箱</span>
                        </v-tooltip>
                    </template>
                    <v-tooltip bottom>
                        <template v-slot:activator="{ on }">
                            <v-btn fab dark small color="indigo" v-on="on" @click="beforeAnswerQuestion">
                                <v-icon>mdi-plus</v-icon>
                            </v-btn>
                        </template>
                        <span>添加回答</span>
                    </v-tooltip>
                    <v-tooltip v-if="authorityJudgment(questionInfo.createUserID)" bottom>
                        <template v-slot:activator="{ on }">
                            <v-btn fab dark small color="green" v-on="on" @click="beforeEditQuestion">
                                <v-icon>mdi-pencil</v-icon>
                            </v-btn>
                        </template>
                        <span>编辑问题</span>
                    </v-tooltip>
                    <v-tooltip v-if="authorityJudgment(questionInfo.createUserID)" bottom>
                        <template v-slot:activator="{ on }">
                            <v-btn fab dark small color="red" v-on="on" @click="beforeDeleteQuestion">
                                <v-icon>mdi-delete</v-icon>
                            </v-btn>
                        </template>
                        <span>删除问题</span>
                    </v-tooltip>
                </v-speed-dial>
            </v-card>
        </v-expand-transition>
        <!--        问题编辑-->
        <v-expand-transition>
            <v-card v-show="questionEdit">
                <v-container fluid>
                    <v-list-item>
                        <v-list-item-content>
                            <v-form v-model="QuestionEditFormValid">
                                <div class="overline mb-4">问题编辑</div>
                                <v-text-field v-model="QuestionEditForm.title" :rules="rules.title" label="问题标题*"
                                              color="amber darken-3" placeholder="请输入问题标题" required :counter="30"
                                              outlined/>
                                <quill-editor :options="editorOption" v-model="QuestionEditForm.content"/>
                            </v-form>
                        </v-list-item-content>
                    </v-list-item>
                    <v-card-actions>
                        <v-spacer/>
                        <v-btn color="grey lighten-1" text @click="questionEdit = false">取消</v-btn>
                        <v-btn :disabled="!QuestionEditFormValid" color="amber darken-3" text @click="editQuestion">
                            确认修改
                        </v-btn>
                    </v-card-actions>
                </v-container>
            </v-card>
        </v-expand-transition>
        <!--        创建回答-->
        <v-expand-transition>
            <v-card v-show="createAnswerExpand" class="mx-auto" style="margin-top: 1rem">
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
                                    <quill-editor :options="editorOption" v-model="AnswerForm.content"/>
                                </v-flex>
                            </v-layout>
                        </v-form>
                    </v-container>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="grey lighten-1" text @click="createAnswerExpand = false">取消</v-btn>
                    <v-btn text color="amber darken-3" @click="answerQuestion">发布回答</v-btn>
                </v-card-actions>
            </v-card>
        </v-expand-transition>
        <!--        回答列表-->
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
                    <v-scroll-y-reverse-transition>
                        <div v-if="!item.isEditing" v-html="item.content"></div>
                        <quill-editor v-else :options="editorOption" v-model="AnswerEditForm.content"/>
                    </v-scroll-y-reverse-transition>
                    <v-card-actions style="margin-top: 1rem; margin-bottom: -0.5rem">
                        <v-tooltip v-if="authorityJudgment(item.createUserID)" bottom>
                            <template v-slot:activator="{ on }">
                                <v-btn text fab small color="grey darken-1" v-on="on" :disabled="answerEditing"
                                       @click="beforeEditAnswer(index)">
                                    <v-icon>mdi-pencil</v-icon>
                                </v-btn>
                            </template>
                            <span>编辑回答</span>
                        </v-tooltip>
                        <v-tooltip v-if="authorityJudgment(item.createUserID)" bottom>
                            <template v-slot:activator="{ on }">
                                <v-btn text fab small color="grey darken-1" v-on="on"
                                       @click="deleteAnswer(item.answerID)">
                                    <v-icon>mdi-delete</v-icon>
                                </v-btn>
                            </template>
                            <span>删除回答</span>
                        </v-tooltip>
                        <v-spacer></v-spacer>
                        <v-btn v-show="item.isEditing" color="grey lighten-1" text @click="afterEditAnswer(index)">取消</v-btn>
                        <v-btn v-show="item.isEditing" color="amber darken-3" text @click="editAnswer(index)">
                            确认修改
                        </v-btn>
                    </v-card-actions>
                </v-expansion-panel-content>
            </v-expansion-panel>
        </v-expansion-panels>
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
        <v-dialog v-model="messageDialogShow" persistent max-width="290">
            <v-card>
                <v-card-title class="headline">{{messageDialogTitle}}</v-card-title>
                <v-card-text>{{messageDialogMessage}}</v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="amber darken-3" text @click="dialogBackToHome?backToHome():messageDialogShow = false">
                        好的
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-snackbar v-model="snackBarShow">
            {{ snackBarMessage }}
            <v-btn color="amber" text @click="snackBarShow = false">
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
    import {
        AnswerQuestion,
        AnswersInfo,
        DeleteAnswer,
        DeleteQuestion,
        EditAnswer,
        EditQuestion,
        QuestionsInfo
    } from "../assets/js/url";

    export default {
        components: {
            quillEditor
        },
        data: () => ({
            questionID: 0,
            answerIDToDel: 0,
            questionInfo: [],
            answerList: [],
            AnswerForm: {
                content: ''
            },
            QuestionEditForm: {
                title: '',
                content: ''
            },
            QuestionEditFormValid: false,
            AnswerEditForm: {
                content: ''
            },
            questionEdit: false,
            answerEditing: false,
            floatButtonClicked: false,
            createAnswerExpand: false,
            messageDialogShow: false,
            messageDialogTitle: '',
            messageDialogMessage: '',
            askDialogShow: false,
            askDialogTitle: '',
            askDialogMessage: '',
            askDialogToDo: '',
            dialogBackToHome: false,
            snackBarShow: false,
            snackBarMessage: '',
            rules: {
                title: [
                    v => !!v || '问题标题不得为空',
                    v => (v && v.length >= 5 && v.length <= 30) || '问题标题应大于5个字符,小于30个字符'
                ]
            },
            editorOption: {
                modules: {
                    toolbar: [
                        ['bold', 'italic', 'underline', 'strike'],
                        [{'header': 1}, {'header': 2}],
                        [{'list': 'ordered'}, {'list': 'bullet'}],
                        [{'script': 'sub'}, {'script': 'super'}],
                        [{'header': [1, 2, 3, 4, 5, 6, false]}],
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
                                this.QuestionEditForm.title = this.questionInfo.title;
                                this.QuestionEditForm.content = this.questionInfo.content;
                            }
                        }
                    )
            },
            getAnswers() {
                axios.get(AnswersInfo + this.questionID)
                    .then(
                        res => {
                            if (res.data.status === 200) {
                                let data = res.data.data;
                                for (let elem of data) {
                                    elem['isEditing'] = false;
                                }
                                console.log(data)
                                this.answerList = data;
                            }
                        }
                    )
            },
            authorityJudgment(accessUserID) {
                return accessUserID + '' === this.currentUserID;
            },
            answerQuestion() {
                let formData = new FormData();
                formData.append('content', this.AnswerForm.content);
                axios.post(AnswerQuestion + this.questionID, formData).then(
                    res => {
                        if (res.data.status === 200) {
                            this.snackBarShow = true;
                            this.snackBarMessage = "回答发布成功！";
                            this.AnswerForm.content = '';
                            this.createAnswerExpand = false
                            this.getAnswers();
                        } else {
                            this.messageDialogShow = true;
                            this.messageDialogTitle = "发布失败";
                            this.messageDialogMessage = res.data.message;
                            this.dialogBackToHome = false;
                        }
                    }
                )
            },
            editQuestion() {
                let formData = new FormData();
                formData.append('title', this.QuestionEditForm.title);
                formData.append('content', this.QuestionEditForm.content);
                axios.post(EditQuestion + this.questionID, formData).then(
                    res => {
                        if (res.data.status === 200) {
                            this.snackBarShow = true;
                            this.snackBarMessage = "问题编辑成功！";
                            this.questionEdit = false;
                            this.getQuestionInfo();
                        } else {
                            this.messageDialogShow = true;
                            this.messageDialogTitle = "问题编辑失败";
                            this.messageDialogMessage = res.data.message;
                            this.dialogBackToHome = false;
                            this.getQuestionInfo();
                        }
                    }
                )
            },
            beforeEditQuestion() {
                // this.floatButtonClicked = false;
                this.$refs.fabButton.click();
                this.questionEdit = true

            },
            beforeAnswerQuestion() {
                // this.floatButtonClicked = false;
                this.$refs.fabButton.click();
                this.createAnswerExpand = true
            },
            beforeDeleteQuestion() {
                // this.floatButtonClicked = false;
                this.$refs.fabButton.click();
                this.askDialogShow = true;
                this.askDialogTitle = "删除问题";
                this.askDialogMessage = "您确定要删除这个问题吗";
                this.askDialogToDo = "deleteQuestion";
            },
            beforeEditAnswer(index) {
                this.answerList[index].isEditing = true;
                this.AnswerEditForm.content = this.answerList[index].content;
                this.answerEditing = true;
            },
            afterEditAnswer(index) {
                this.answerList[index].isEditing = false;
                this.answerEditing = false;
            },
            editAnswer(index) {
                let formData = new FormData();
                formData.append('content', this.AnswerEditForm.content);
                axios.post(EditAnswer + this.answerList[index].answerID, formData).then(
                    res => {
                        if (res.data.status === 200) {
                            this.snackBarShow = true;
                            this.snackBarMessage = "答案编辑成功！";
                            this.afterEditAnswer(index);
                            this.getAnswers();
                        } else {
                            this.messageDialogShow = true;
                            this.messageDialogTitle = "答案编辑失败";
                            this.messageDialogMessage = res.data.message;
                            this.dialogBackToHome = false;
                        }
                    }
                )
            },
            deleteAnswer(answerID) {
                this.answerIDToDel = answerID;
                this.askDialogShow = true;
                this.askDialogTitle = "删除答案";
                this.askDialogMessage = "您确定要删除这个答案吗";
                this.askDialogToDo = "deleteAnswer";
            },
            askDialogAction() {
                if (this.askDialogToDo === "deleteQuestion") {
                    this.askDialogShow = false;
                    axios.get(DeleteQuestion + this.questionID)
                        .then(
                            res => {
                                if (res.data.status === 200) {
                                    this.messageDialogShow = true;
                                    this.messageDialogTitle = "删除成功";
                                    this.messageDialogMessage = "点击确定将跳转到首页";
                                    this.dialogBackToHome = true;
                                }
                            }
                        )
                } else if (this.askDialogToDo === "deleteAnswer") {
                    this.askDialogShow = false;
                    axios.get(DeleteAnswer + this.answerIDToDel)
                        .then(
                            res => {
                                if (res.data.status === 200) {
                                    this.snackBarShow = true;
                                    this.snackBarMessage = "回答删除成功！";
                                    this.getAnswers();
                                } else {
                                    this.messageDialogShow = true;
                                    this.messageDialogTitle = "删除失败";
                                    this.messageDialogMessage = res.data.message;
                                    this.dialogBackToHome = false;
                                }
                            }
                        )
                } else {
                    this.askDialogShow = false;
                }

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
