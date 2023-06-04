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
      test: /\.css$/,
      use: [
        'style-loader',
        'css-loader'
      ]
    }
  ]},
};