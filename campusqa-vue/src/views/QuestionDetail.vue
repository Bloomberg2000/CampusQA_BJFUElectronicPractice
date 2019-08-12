<template>
    <div class="questiondetail" style="height:auto ; width: auto">
        <v-speed-dial
                v-model="fab"
                bottom="true" right="true"
                direction="top"
                transition="slide-y-reverse-transition"
        >
            <template v-slot:activator>
                <v-btn v-model="fab" color="blue darken-2" dark fab>
                    <v-icon v-if="fab">close</v-icon>
                    <v-icon v-else>account_circle</v-icon>
                </v-btn>
            </template>
            <v-btn fab dark small color="green">
                <v-icon>edit</v-icon>
            </v-btn>
            <v-btn fab dark small color="indigo">
                <v-icon>add</v-icon>
            </v-btn>
            <v-btn fab dark small color="red">
                <v-icon>delete</v-icon>
            </v-btn>
        </v-speed-dial>
    </div>
</template>
<script>
    export default {
        data: () => ({
            fab: false,
            fling: false,
            hover: false,
            tabs: null,
            top: false,
            right: true,
            bottom: true,
            left: false,
            transition: 'slide-y-reverse-transition',
        }),

        computed: {
            activeFab() {
                switch (this.tabs) {
                    case 'one':
                        return {class: 'purple', icon: 'account_circle'}
                    case 'two':
                        return {class: 'red', icon: 'edit'}
                    case 'three':
                        return {class: 'green', icon: 'keyboard_arrow_up'}
                    default:
                        return {}
                }
            },
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
            },
        },
    }
</script>
Options
<style>
    /* This is for documentation purposes and will not be needed in your application */
    #create .v-speed-dial {
        position: absolute;
    }

    #create .v-btn--floating {
        position: relative;
    }
</style>
