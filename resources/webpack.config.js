const path = require('path');

module.exports = {
    entry: './js/index.js',
    output: {
        path: path.resolve(__dirname, 'result'),
        filename: '../../website/static/assets/js/script.min.js'
    },
    module: {
        rules: [{
            test: /\.css$/i,
            loader: 'css-loader',
            options: {
                modules: true,
            },
        }, ],
    },
};