<template>
    <div class="questiondetail">
        <v-card id="create">
            <v-container fluid>
                <v-list-item>
                    <v-list-item-content>
                        <!--          <div class="overline mb-4">OVERLINE</div>-->
                        <v-list-item-title class="headline mb-1">问题标题</v-list-item-title>
                        <v-list-item-subtitle><p>sjxnsanxakxjnaskx</p>

                        </v-list-item-subtitle>
                        <v-list-item-content>
                            <h1>x sa x a c m s l d c m s l d k c m s l c</h1>
                            <p>dskmc</p>
                            <p>cs</p>
                            <p>cdsckdscsc</p>
                            <p>cddcdc<sub>23</sub></p>
                            <p><sub><strong><em><s><u>cdsmclsmdkm</u></s></em></strong><s><span
                                    class="ql-cursor"></span></s></sub></p>
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
            <v-expansion-panel v-for="(item,i) in 20" :key="i">
                <v-expansion-panel-header>Item<br><br></v-expansion-panel-header>
                <v-expansion-panel-content>
                    <h1>x sa x a c m s l d c m s l d k c m s l c</h1>
                    <p>dskmc</p>
                    <p>cs</p>
                    <p>cdsckdscsc</p>
                    <p>cddcdc<sub>23</sub></p>
                    <p><sub><strong><em><s><u>cdsmclsmdkm</u></s></em></strong><s><span
                            class="ql-cursor"></span></s></sub></p>
                </v-expansion-panel-content>
            </v-expansion-panel>
        </v-expansion-panels>
    </div>
</template>
<script>
    export default {
        data: () => ({
            fab: false
        }),
        computed: {},
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
            },
        },
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
