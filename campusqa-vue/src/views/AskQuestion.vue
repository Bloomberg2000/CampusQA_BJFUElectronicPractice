<template>
    <div class="askquestion" style="margin-top: 15px">
        <v-card outlined>
            <v-card-title>
                <span class="headline">我要提问</span>
            </v-card-title>
            <v-card-text>
                <v-container grid-list-md>
                    <v-form ref="form" v-model="formValid">
                        <v-layout wrap>
                            <v-flex xs12>
                                <v-text-field v-model="QuestionForm.title" :rules="rules.title" label="问题标题*"
                                              color="amber darken-3" placeholder="请输入问题标题" required :counter="30"
                                              outlined/>
                            </v-flex>
                            <v-flex xs12>
                                <small style="position:absolute;margin-left:13px;margin-top: -10px;background-color: #ffffff">
                                    问题描述*
                                </small>
                                <quill-editor ref="myQuillEditor" :options="editorOption"
                                              v-model="QuestionForm.describe"/>
                            </v-flex>
                        </v-layout>
                    </v-form>
                </v-container>
            </v-card-text>
            <v-card-actions>
                <v-spacer/>
                <v-btn :disabled="!formValid" color="amber darken-3" text @click="askQuestion">发布问题</v-btn>
            </v-card-actions>
        </v-card>
        <v-dialog v-model="errorDialogShow" persistent max-width="290">
            <v-card>
                <v-card-title class="headline">发布失败</v-card-title>
                <v-card-text>{{errorDialogMessage}}</v-card-text>
                <v-card-actions>
                    <v-spacer/>
                    <v-btn color="amber darken-3" text @click="errorDialogShow = false">好的</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>
<script>
    import 'quill/dist/quill.core.css';
    import 'quill/dist/quill.snow.css';
    import 'quill/dist/quill.bubble.css';
    import {quillEditor} from "vue-quill-editor"; //调用编辑器
    import {AskQuestion} from "../assets/js/url";
    import axios from 'axios'

    export default {
        components: {
            quillEditor
        },
        data: () => ({
            errorDialogShow: false,
            errorDialogMessage: '',
            formValid: true,
            QuestionForm: {
                title: '',
                describe: ''
            },
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
                placeholder: '请输入问题描述*'
            }
        }),
        computed: {
            editor() {
                return this.$refs.myQuillEditor.quill;
            },
        },
        mounted() {
            // 设置编辑器高度
            this.editor.container.style.height = `350px`
        },
        methods: {
            askQuestion() {
                let formData = new FormData();
                formData.append('title', this.QuestionForm.title);
                formData.append('content', this.QuestionForm.describe);
                axios.post(AskQuestion, formData).then(
                    res => {
                        if (res.data.status === 200) {
                            this.$router.push({
                                path: "/questiondetail",
                                query: {
                                    questionID: res.data.data.questionID
                                }
                            });
                        } else {
                            this.errorDialogShow = true;
                            this.errorDialogMessage = res.data.message;
                        }
                    }
                )
            },
        }
    }
</script>

<style>
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
