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
                        <v-form ref="form" style="padding:20px">
                            <v-layout wrap>
                                <v-flex xs12 sm6 style="padding:2px">
                                    <v-text-field :disabled="!edit" v-model="editForm.name" :rules="rules.name"
                                                  label="姓名*"
                                                  :counter="10" color="amber darken-3" required outlined/>
                                </v-flex>
                                <v-flex xs12 sm6 style="padding:2px">
                                    <v-select :disabled="!edit" v-model="editForm.gender" :rule="rules.gender"
                                              :items="['男', '女']" label="性别*"
                                              color="amber darken-3" required outlined/>
                                </v-flex>
                                <v-flex xs12 sm6 style="padding:2px">
                                    <v-text-field :disabled="!edit" v-model="editForm.enrollmentTime"
                                                  :rules="rules.enrollmentTime"
                                                  label="入学年份*" color="amber darken-3" required outlined/>
                                </v-flex>
                                <v-flex xs12 sm6 style="padding:2px">
                                    <v-autocomplete :disabled="!edit" v-model="editForm.college" :rules="rules.college"
                                                    :items="['林学院' ,'水土保持学院' ,'生物科学与技术学院' ,'园林学院' ,
                                                    '经济管理学院' ,'工学院' ,'材料科学与技术学院' ,'人文社会科学学院' ,
                                                    '外语学院' ,'信息学院' ,'理学院' ,'自然保护区学院' ,'环境科学与工程学院' ,
                                                    '艺术设计学院' ,'马克思主义学院' ,'草业与草原学院' ,'继续教育学院' ,'国际学院' ,'体育教学部']"
                                                    label="学院" color="amber darken-3" outlined/>
                                </v-flex>
                                <v-flex xs12 sm6 style="padding:2px">
                                    <v-text-field :disabled="!edit" v-model="editForm.phoneNum" :rules="rules.phoneNum"
                                                  label="电话号码*" color="amber darken-3" required outlined/>
                                </v-flex>
                            </v-layout>
                        </v-form>
                        <v-card-actions style="padding: 0 15px 15px 15px">
                            <v-spacer/>
                            <v-btn v-show="!edit" text color="amber" @click="edit = true">编辑资料</v-btn>
                            <v-btn v-show="edit" text color="amber" @click="edit = false">取消</v-btn>
                            <v-btn v-show="edit" text color="amber" @click="doEdit">保存</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-tab-item>
                <v-tab-item>
                    <PersonalQuestions/>
                </v-tab-item>
                <v-tab-item>
                    <PersonalAnswers/>
                </v-tab-item>
            </v-tabs>
        </v-card>
        <v-snackbar v-model="snackBarShow">
            {{ snackBarMessage }}
            <v-btn color="amber" text @click="snackBarShow = false">
                关闭
            </v-btn>
        </v-snackbar>
    </div>
</template>
<script>
    import axios from 'axios'
    const PersonalQuestions = () => import('../components/PersonalQuestions');
    const PersonalAnswers = () => import('../components/PersonalAnswers');
    import {EditUserInfo, UserInfo} from "../assets/js/url";

    export default {
        components: {
            PersonalQuestions, PersonalAnswers
        },
        data: () => ({
            personalInfo: '',
            personalAnswerList: [],
            snackBarShow: false,
            snackBarMessage: '',
            edit: false,
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
            },
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
            tabChange(tabNum) {
                switch (tabNum) {
                    case 0:
                        this.getPersonalInfo();
                        break;
                }
            },
            doEdit() {
                let formData = new FormData();
                formData.append('name', this.editForm.name);
                formData.append('gender', this.editForm.gender);
                formData.append('college', this.editForm.college);
                formData.append('phoneNum', this.editForm.phoneNum);
                formData.append('enrollmentTime', this.editForm.enrollmentTime);
                axios.post(EditUserInfo, formData).then(
                    res => {
                        if (res.data.status === 200) {
                            this.snackBarShow = true;
                            this.snackBarMessage = "保存成功！";
                            this.edit = false;
                        } else {
                            this.snackBarShow = true;
                            this.snackBarMessage = "保存失败！" + res.data.message;
                        }
                    }
                )
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
