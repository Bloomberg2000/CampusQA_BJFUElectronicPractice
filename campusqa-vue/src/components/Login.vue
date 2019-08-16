<template>
    <v-layout justify-center>
        <v-dialog v-model="loginModalShow" persistent max-width="600px">
            <template v-slot:activator="{ on }">
                <v-list-item link v-on="on" color="amber darken-3">
                    <v-list-item-action>
                        <v-icon>mdi-login</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title class="grey--text">登录</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </template>
            <v-card>
                <v-card-title>
                    <span class="headline">登录</span>
                </v-card-title>
                <v-card-text>
                    <v-container grid-list-md>
                        <v-form ref="form" v-model="formValid">
                            <v-layout wrap>
                                <v-flex xs12>
                                    <v-text-field v-model="LoginForm.phoneNum" :rules="rules.phoneNum" label="电话号码*"
                                                  color="amber darken-3" required/>
                                </v-flex>
                                <v-flex xs12>
                                    <v-text-field v-model="LoginForm.password" :rules="rules.password" label="密码*"
                                                  type="password" color="amber darken-3" required/>
                                </v-flex>
                            </v-layout>
                        </v-form>
                    </v-container>
                    <small>*为必填项</small>
                </v-card-text>
                <v-card-actions>
                    <v-spacer/>
                    <v-btn color="amber darken-3" text @click="close">关闭</v-btn>
                    <v-btn color="amber darken-3" :disabled="!formValid" text @click="login">登录</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-dialog v-model="errorDialogShow" persistent max-width="290">
            <v-card>
                <v-card-title class="headline">登录失败</v-card-title>
                <v-card-text>{{errorDialogMessage}}</v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="amber darken-3" text @click="errorDialogShow = false">好的</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-layout>
</template>
<script>
    import axios from 'axios'
    import {Login} from "../assets/js/url";

    export default {
        data: () => ({
            formValid: true,
            loginModalShow: false,
            errorDialogShow: false,
            errorDialogMessage: '',
            LoginForm: {
                phoneNum: '',
                password: ''
            },
            rules: {
                phoneNum: [
                    v => !!v || '请输入电话号码',
                    v => /^1[3456789]\d{9}$/.test(v) || '电话号码格式不正确'
                ],
                password: [
                    v => !!v || '请输入密码'
                ]
            }
        }),
        methods: {
            close() {
                this.LoginForm.phoneNum = '';
                this.LoginForm.password = '';
                this.$refs.form.reset();
                this.loginModalShow = false;
            },
            login() {
                let formData = new FormData();
                formData.append('phoneNum', this.LoginForm.phoneNum);
                formData.append('password', this.LoginForm.password);
                axios.post(Login, formData).then(
                    res => {
                        if (res.data.status === 200) {
                            this.$store.commit("userChange", res.data.data.userID + '');
                            this.close();
                        } else {
                            this.errorDialogShow = true;
                            this.errorDialogMessage = res.data.message;
                        }
                    }
                )
            }
        }
    }
</script>
