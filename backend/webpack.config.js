const nodeExternals = require('webpack-node-externals');

module.exports = function (options) {
  return {
    ...options,
    output: {
      ...options.output,
      libraryTarget: 'commonjs2',
    },
    externals: [
      nodeExternals({
        allowlist: [/^@nestjs\/(config|jwt|passport)/],
      }),
    ],
  };
};
