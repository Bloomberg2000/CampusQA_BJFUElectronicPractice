<template>
    <div class="home" style="margin-top: 15px">
        <v-card outlined class="mx-auto" style="margin-top: 10px;margin-bottom: 15px">
            <v-list-item three-line>
                <v-list-item-content>
                    <!--          <div class="overline mb-4">OVERLINE</div>-->
                    <v-list-item-title class="headline mb-1">问题标题</v-list-item-title>
                    <v-list-item-subtitle>问题描述</v-list-item-subtitle>
                </v-list-item-content>

                <v-list-item-avatar tile size="80" color="grey"></v-list-item-avatar>
            </v-list-item>

            <v-card-actions style="margin-left: 10px">
                <v-btn outlined to="/questiondetail">查看问题</v-btn>
                <v-spacer></v-spacer>
<!--                <v-btn icon>-->
<!--                    <v-icon>mdi-heart</v-icon>-->
<!--                </v-btn>-->
            </v-card-actions>
        </v-card>
        <v-spacer></v-spacer>
    </div>
</template>
