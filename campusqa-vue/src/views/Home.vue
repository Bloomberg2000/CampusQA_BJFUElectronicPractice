<template>
    <div class="home" style="margin-top: 15px">
        <div class="list">
            <v-hover v-slot:default="{ hover }">
                <v-card :elevation="hover ? 12 : 2" outlined class="mx-auto"
                        style="margin-top: 10px;margin-bottom: 15px" to="/questiondetail">
                    <v-list-item three-line>
                        <v-list-item-content>
                            <!--          <div class="overline mb-4">OVERLINE</div>-->
                            <v-list-item-title class="headline mb-1">问题标题</v-list-item-title>
                            <v-list-item-subtitle>问题描述</v-list-item-subtitle>
                        </v-list-item-content>
                        <v-list-item-avatar tile size="80" color="grey"></v-list-item-avatar>
                    </v-list-item>
                    <v-card-actions style="margin-right: 10px">
                        <v-spacer></v-spacer>
                        <v-btn outlined to="/questiondetail">查看问题</v-btn>

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
