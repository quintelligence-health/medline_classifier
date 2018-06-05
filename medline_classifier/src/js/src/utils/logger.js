let bunyan = require('bunyan');
let args = require('./arguments');

function extractLogLevel(args) {
    if (args.v != null) {
        return 'trace';
    } else if (args.log != null) {
        return args.log;
    } else {
        return 'info';
    }
}

let level = extractLogLevel(args);

var log = bunyan.createLogger({
    name: 'MeSH Classifier',
    level: level,
    src: args.showline != null
});

log.info('logger initialized using level `%s`', level);

module.exports = exports = log;
