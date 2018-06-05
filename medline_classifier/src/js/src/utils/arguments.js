let path = require('path');
let fs = require('fs');
let args = require('minimist')(process.argv.slice(2));

if (args.h != null) {
    console.log('options:');
    console.log('-h:\tprint help');
    console.log('-v:\tverbose mode');
    console.log('--showline: show line number in logger output');
    console.log('--log: set custom log level');
    console.log('-f $CONF_FILE:\t path to the config file');
    console.log('-w $WORKER_N - index of the worker');
    console.log('--port: port');
    process.exit(0);
}

function parseConfFile() {
    let confFile = path.join(__dirname, '../../config/config.json');

    if (args.conf != null) {
        confFile = path.join(__dirname, '../..', args.conf);
    }

    let settingsStr = fs.readFileSync(confFile);
    let settings = JSON.parse(settingsStr);
    return settings;
}

args.settings = parseConfFile();

module.exports = exports = args;
