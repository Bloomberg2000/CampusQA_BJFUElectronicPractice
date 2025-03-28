const path = require("path");

function resolve(dir) {
    return path.join(__dirname, dir);
}

module.exports = {
    //基本路径
    publicPath: './',//vue-cli3.3+新版本使用
    //输出文件目录
    outputDir: 'dist',
    // eslint-loader 是否在保存的时候检查
    lintOnSave: true,
    // 放置生成的静态资源 (js、css、img、fonts) 的 (相对于 outputDir 的) 目录。
    assetsDir: 'static',
    // 以多页模式构建应用程序。
    pages: undefined,
    //是否使用包含运行时编译器的 Vue 构建版本
    runtimeCompiler: false,
    //是否为 Babel 或 TypeScript 使用 thread-loader。该选项在系统的 CPU 有多于一个内核时自动启用，仅作用于生产构建，在适当的时候开启几个子进程去并发的执行压缩
    parallel: require('os').cpus().length > 1,
    //生产环境是否生成 sourceMap 文件，一般情况不建议打开
    productionSourceMap: false,
    // webpack配置
    //对内部的 webpack 配置进行更细粒度的修改 https://github.com/neutrinojs/webpack-chain see https://github.com/vuejs/vue-cli/blob/dev/docs/webpack.md
    chainWebpack: config => {
        config.module
            .rule('images')
            .use('image-webpack-loader')
            .loader('image-webpack-loader')
            .options({
                bypassOnDebug: true
            })
            .end();
        config.resolve.alias
            .set("@$", resolve("src"))
            .set("assets", resolve("src/assets"))
            .set("components", resolve("src/components"))
            .set("base", resolve("baseConfig"))
            .set("public", resolve("public"));
    },

    //调整 webpack 配置 https://cli.vuejs.org/zh/guide/webpack.html#%E7%AE%80%E5%8D%95%E7%9A%84%E9%85%8D%E7%BD%AE%E6%96%B9%E5%BC%8F
    configureWebpack:
        () => ({
            // optimization: {
            //     splitChunks: {
            //         cacheGroups: {
            //             vendor: {
            //                 chunks: "all",
            //                 test: /node_modules/,
            //                 name: "vendor",
            //                 minChunks: 1,
            //                 maxInitialRequests: 5,
            //                 minSize: 0,
            //                 priority: 100,
            //             },
            //             common: {
            //                 chunks: "all",
            //                 test: /[\\/]src[\\/]js[\\/]/,
            //                 name: "common",
            //                 minChunks: 2,
            //                 maxInitialRequests: 5,
            //                 minSize: 0,
            //                 priority: 60
            //             },
            //             styles: {
            //                 name: 'styles',
            //                 test: /\.(sa|sc|c)ss$/,
            //                 chunks: 'all',
            //                 enforce: true,
            //             },
            //             runtimeChunk: {
            //                 name: 'manifest'
            //             }
            //         }
            //     }
            // }
        }),
    css:
        {
            // 是否使用css分离插件
            extract: true,
            // 开启 CSS source maps，一般不建议开启
            sourceMap:
                false,
            modules:
                false,
            // css预设器配置项
            loaderOptions:
                {}
        }
    ,
// webpack-dev-server 相关配置 https://webpack.js.org/configuration/dev-server/
    devServer: {
        host: "0.0.0.0",
        port:
            8080, // 端口号
        https:
            false, // https:{type:Boolean}
        open:
            true, //配置自动启动浏览器  http://172.16.1.12:7071/rest/mcdPhoneBar/
        hotOnly:
            true, // 热更新
        // proxy: 'http://localhost:8080'   // 配置跨域处理,只有一个代理
        proxy:
            { // 配置自动启动浏览器
                "/campusqa":
                    {
                        target: "http://0.0.0.0:8000/",
                        changeOrigin:
                            true,
                        // ws: true,//websocket支持
                        secure:
                            false
                    }
            }
    }
    ,
// 第三方插件配置 https://www.npmjs.com/package/vue-cli-plugin-style-resources-loader
    pluginOptions: {
        'style-resources-loader':
            {//https://github.com/yenshih/style-resources-loader
                preProcessor: 'scss',//声明类型
                'patterns':
                    [
                        //path.resolve(__dirname, './src/assets/scss/_common.scss'),
                    ],
                //injector: 'append'
            }
    }
    ,
}
;
