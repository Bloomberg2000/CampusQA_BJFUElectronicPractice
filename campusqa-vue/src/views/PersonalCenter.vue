<template>
    <div>
        <v-card class="mx-auto" tile>
            <v-parallax :src="imgpath.public.profile" height="300">
                <v-row align="center" justify="center" class="fill-height">
                    <v-avatar class="profile" color="grey" size="164" style="margin-top: 1.5rem">
                        <v-img :src="imgpath.public.userPic"></v-img>
                    </v-avatar>
                </v-row>
                <v-row align="center" justify="center" class="fill-height">
                    <v-list-item color="rgba(0, 0, 0, .4)" dark align="center">
                        <v-list-item-content>
                            <v-list-item-title class="title">{{personalInfo.name}}</v-list-item-title>
                            <v-list-item-subtitle>{{personalInfo.college}} {{personalInfo.enrollmentTime}}级学生
                            </v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>
                </v-row>
            </v-parallax>
            <v-tabs fixed-tabs background-color="white" color="amber" @change="tabChange">
                <v-tab>我</v-tab>
                <v-tab>我的提问</v-tab>
                <v-tab>我的回答</v-tab>
                <v-tab-item>
                    <v-card>
                        <v-card-text>我的资料</v-card-text>
                        <v-form ref="form">
                            <v-layout wrap>
                                <v-flex xs12 sm6>
                                    <v-text-field v-model="editForm.name" :rules="rules.name" label="姓名*"
                                                  :counter="10" color="amber darken-3" required/>
                                </v-flex>
                                <v-flex xs12 sm6>
                                    <v-select v-model="editForm.gender" :rule="rules.gender"
                                              :items="['男', '女']" label="性别*"
                                              color="amber darken-3" required/>
                                </v-flex>
                                <v-flex xs12 sm6>
                                    <v-text-field v-model="editForm.enrollmentTime" :rules="rules.enrollmentTime"
                                                  label="入学年份*" color="amber darken-3" required/>
                                </v-flex>
                                <v-flex xs12 sm6>
                                    <v-autocomplete v-model="editForm.college" :rules="rules.college"
                                                    :items="['信息学院', '理学院', '环境科学与技术学院','林学院','园林学院','草原与草业学院']"
                                                    label="学院" color="amber darken-3"/>
                                </v-flex>
                                <v-flex xs12 sm6>
                                    <v-text-field v-model="editForm.phoneNum" :rules="rules.phoneNum"
                                                  label="电话号码*" color="amber darken-3" required/>
                                </v-flex>
                            </v-layout>
                        </v-form>
                    </v-card>
                </v-tab-item>
                <v-tab-item>
                    <v-card flat>
                        <v-card-text>234</v-card-text>
                    </v-card>
                </v-tab-item>
                <v-tab-item>
                    <v-card flat>
                        <v-card-text>456</v-card-text>
                    </v-card>
                </v-tab-item>
            </v-tabs>
        </v-card>
    </div>
</template>
<script>
    import axios from 'axios'
    import {UserAnswerList, UserInfo, UserQuestionList} from "../assets/js/url";

    export default {
        data: () => ({
            personalInfo: '',
            personalQuestionList: [],
            personalAnswerList: [],
            editForm: {
                name: '',
                gender: '',
                college: '',
                phoneNum: '',
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
            getPersonalInfo() {
                axios.get(UserInfo + this.userID)
                    .then(
                        res => {
                            if (res.data.status === 200) {
                                this.personalInfo = res.data.data[0];
                                this.editForm.name = res.data.data[0].name;
                                this.editForm.gender = res.data.data[0].gender;
                                this.editForm.college = res.data.data[0].college;
                                this.editForm.phoneNum = res.data.data[0].phoneNum;
                                this.editForm.enrollmentTime = res.data.data[0].enrollmentTime;
                                console.log(this.personalInfo);
                            }
                        }
                    )
            },
            getPersonalQuestionList() {
                axios.get(UserQuestionList + this.userID)
                    .then(
                        res => {
                            if (res.data.status === 200) {
                                this.personalQuestionList = res.data.data[0];
                                console.log(this.personalQuestionList);
                            }
                        }
                    )
            },
            getPersonalAnswerList() {
                axios.get(UserAnswerList + this.userID)
                    .then(
                        res => {
                            if (res.data.status === 200) {
                                this.personalAnswerList = res.data.data[0];
                                console.log(this.personalAnswerList);
                            }
                        }
                    )
            },
            tabChange(tabNum) {
                switch (tabNum) {
                    case 0:
                        this.getPersonalInfo();
                        break;
                    case 1:
                        this.getPersonalQuestionList();
                        break;
                    case 2:
                        this.getPersonalAnswerList();
                        break;
                }
            }
        },
        computed: {
            imgpath() {
                return this.$store.state.imageStyle
            },
            userID() {
                return this.$route.query.userID;
            },
        }
    }
</script>
<style>

</style>
