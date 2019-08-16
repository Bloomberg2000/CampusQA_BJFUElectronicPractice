<template>
    <v-layout justify-center>
        <v-dialog v-model="registerModalShow" persistent max-width="600px">
            <template v-slot:activator="{ on }">
                <v-list-item link v-on="on">
                    <v-list-item-action>
                        <v-icon>mdi-account-check</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title class="grey--text">注册</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </template>
            <v-card>
                <v-card-title>
                    <span class="headline">注册</span>
                </v-card-title>
                <v-card-text>
                    <v-container grid-list-md>
                        <v-form ref="form" v-model="valid">
                            <v-layout wrap>
                                <v-flex xs12 sm6>
                                    <v-text-field v-model="registerForm.name" :rules="rules.name" label="姓名*"
                                                  :counter="10" color="amber darken-3" required/>
                                </v-flex>
                                <v-flex xs12 sm6>
                                    <v-select v-model="registerForm.gender" :rule="rules.gender"
                                              :items="['男', '女']" label="性别*"
                                              color="amber darken-3" required/>
                                </v-flex>
                                <v-flex xs12 sm6>
                                    <v-text-field v-model="registerForm.enrollmentTime" :rules="rules.enrollmentTime"
                                                  label="入学年份*" color="amber darken-3" required/>
                                </v-flex>
                                <v-flex xs12 sm6>
                                    <v-autocomplete v-model="registerForm.college" :rules="rules.college"
                                                    :items="['信息学院', '理学院', '环境科学与技术学院','林学院','园林学院','草原与草业学院']"
                                                    label="学院" color="amber darken-3"/>
                                </v-flex>
                                <v-flex xs12 sm6>
                                    <v-text-field v-model="registerForm.phoneNum" :rules="rules.phoneNum"
                                                  label="电话号码*" color="amber darken-3" required/>
                                </v-flex>
                                <v-flex xs12 sm6>
                                    <v-text-field v-model="registerForm.password" :rules="rules.password"
                                                  label="密码*" color="amber darken-3" type="password"
                                                  required hint="密码需8位及以上，包含数字、字母"/>
                                </v-flex>
                            </v-layout>
                        </v-form>
                    </v-container>
                    <small>*为必填项</small>
                </v-card-text>
                <v-card-actions>
                    <v-spacer/>
                    <v-btn color="amber darken-3" text @click="close">关闭</v-btn>
                    <v-btn color="amber darken-3" text :disabled="!valid" @click="register">注册</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-dialog v-model="messageDialogShow" persistent max-width="290">
            <v-card>
                <v-card-title class="headline">{{messageDialogTitle}}</v-card-title>
                <v-card-text>{{messageDialogMessage}}</v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="amber darken-3" text @click="messageDialogShow = false">好的</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-layout>
</template>
<script>
    import axios from 'axios'
    import {Register} from "../assets/js/url";

    export default {
        data: () => ({
            valid: true,
            registerModalShow: false,
            messageDialogShow: false,
            messageDialogTitle: '',
            messageDialogMessage: '',
            registerForm: {
                name: '',
                gender: '',
                college: '',
                phoneNum: '',
                password: '',
                enrollmentTime: ''
            },
            rules: {
                name: [
                    v => !!v || '请输入姓名',
                    v => (v && v.length <= 10) || '姓名应小于10个字符'
                ],
                gender: [v => !!v || '请输入性别'],
                college: [v => !!v || '请输入学院'],
                phoneNum: [
                    v => !!v || '请输入电话号码',
                    v => /^1[3456789]\d{9}$/.test(v) || '电话号码格式不正确'
                ],
                password: [
                    v => !!v || '请输入密码',
                    v => /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,30}$/.test(v) || '密码需8位及以上，包含数字、字母'
                ],
                enrollmentTime: [
                    v => !!v || '请输入入学年份（如：2017）',
                    v => /^(1949|19[5-9]\d|20\d{2}|2100)$/.test(v) || '入学年份格式不正确'
                ],
            }
        }),
        methods: {
            close() {
                this.registerForm.name = '';
                this.registerForm.gender = '';
                this.registerForm.college = '';
                this.registerForm.phoneNum = '';
                this.registerForm.password = '';
                this.registerForm.enrollmentTime = '';
                this.$refs.form.reset();
                this.registerModalShow = false;
            },
            register() {
                let formData = new FormData();
                formData.append('name', this.registerForm.name);
                formData.append('gender', this.registerForm.gender);
                formData.append('college', this.registerForm.college);
                formData.append('phoneNum', this.registerForm.phoneNum);
                formData.append('password', this.registerForm.password);
                formData.append('enrollmentTime', this.registerForm.enrollmentTime);
                axios.post(Register, formData).then(
                    res => {
                        if (res.data.status === 200) {
                            this.messageDialogTitle = "注册成功";
                            this.messageDialogMessage = "现在可以登录啦";
                            this.messageDialogShow = true;
                            this.close();
                        } else {
                            this.messageDialogTitle = "出错了，请重试";
                            this.messageDialogMessage = res.data.message;
                            this.messageDialogShow = true;
                            // this.close();
                        }
                    }
                )
            },
        }
    }
</script>
