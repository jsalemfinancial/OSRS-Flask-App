const path = require('path');

module.exports = {
  mode: 'development',
  entry: './flaskProj/src/',
  output: {
    filename: 'bundle.js',
    path: path.resolve('./flaskProj', 'static'),
  },
  module: { rules: [
    {
      test: /\.js$/,
      include: [
        path.resolve('./flaskProj', 'src')
      ],
      use: ['babel-loader'],
    },
    {
      test: /\.(scss)$/,
      include: [
        path.resolve('./flaskProj', 'src')
      ],
      use: [{
        // inject CSS to page
        loader: 'style-loader'
      }, {
        // translates CSS into CommonJS modules
        loader: 'css-loader'
      }, {
        // Run postcss actions
        loader: 'postcss-loader',
        options: {
          // `postcssOptions` is needed for postcss 8.x;
          // if you use postcss 7.x skip the key
          postcssOptions: {
            // postcss plugins, can be exported to postcss.config.js
            plugins: function () {
              return [
                require('autoprefixer')
              ];
            }
          }
        }
      }, {
        // compiles Sass to CSS
        loader: 'sass-loader'
      }]
    }
  ]},
};
			   