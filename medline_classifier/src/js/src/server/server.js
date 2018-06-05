const express = require('express');
const timeoutMiddleware = require('connect-timeout');
const expressExit = require('express-graceful-exit');
const bodyParser = require('body-parser');
const path = require('path');

class RenderUtils {

    constructor(opts) {
        let self = this;

        if (opts.log == null) throw new Error('Parameter `log` missing!');

        self._log = opts.log;
    }
}

class HttpServer {

    constructor(opts) {
        let self = this;

        let settings = opts.settings;

        if (opts.settings == null) throw new Error('Parameter `settings` missing!');
        if (opts.log == null) throw new Error('Parameter `log` missing!');

        if (settings.port == null) throw new Error('Parameter `port` missing!');

        self._port = settings.port;

        self._app = express();
        self._log = opts.log;
        self._server = null;

        // init middleware
        self._app.use(expressExit.middleware(self._app));
    }

    init(callback) {
        let self = this;
        let log = self._log;

        log.info('initializing HttpServer on port %d', self._port);
        self._server = self._app.listen(self._port);
        callback();
    }

    shutdown(callback) {
        let self = this;
        let log = self._log;

        try {
            log.info('gracefully shutting down server');
            expressExit.gracefulExitHandler(self._app, self._server, {
                socketio: self._app.settings.socketio,
                callback: function () {
                    log.info('server has shut down!');
                    callback();
                }
            })
        } catch (e) {
            callback(e);
        }
    }
}

class ApiServer extends HttpServer {

    constructor(opts) {
        super(opts);
        let self = this;

        // init express
        self._registeredApis = new Set();
    }

    on(api, action, handler) {
        let self = this;
        let log = self._log;

        let registeredApis = self._registeredApis;

        log.info('registering handler for action `%s`', action);

        if (!registeredApis.has(api)) { throw new Error('Api `' + api + '` not initialized!'); }

        let opts = {
            action: action,
            method: 'POST',
            extractData: req => req.body
        }
        self._app.post(path.join('/', api, action), self._requestHandler(opts, handler));
    }

    initApi(api, opts) {
        if (opts == null) { opts = {}; }

        let self = this;
        let log = self._log;

        let registeredApis = self._registeredApis;

        if (registeredApis.has(api)) { throw new Error('Api `' + api + '` already registered!'); }

        log.info('initializing API `%s` with options: `%s`', api, JSON.stringify(opts));

        self._app.use('/' + api, bodyParser.json({ limit: '50mb' }));
        self._app.use('/' + api, timeoutMiddleware(1000*30));   // on timeout to 30 seconds

        registeredApis.add(api);
    }

    _requestHandler(opts, handler) {
        let self = this;
        let log = self._log;

        let action = opts.action;
        let method = opts.method;
        let extractData = opts.extractData;

        let sendResult = function (result, res) {
            if (result == null) {
                res.sendStatus(204);
                res.end();
            } else {
                res.send(result);
                res.end();
            }
        }

        return function (req, res) {
            try {
                let data = extractData(req);

                if (log.trace())
                    log.trace('processing ' + method + ' `' + action);

                handler.call(this, data, function (e, result) {
                    if (e != null) return self._handleError(e, res);

                    if (log.trace())
                        log.trace('finished ' + method + ' `' + action + '`');

                    sendResult(result, res);
                })
            } catch (e) {
                self._handleError(e, res);
            }
        }
    }

    _handleError(e, res) {
        let self = this;
        let log = self._log;

        log.error(e, 'Exception while handling request!');
        res.status(500);
        res.send({ message: e.message });
        res.end();
    }
}

class StaticAndApiServer extends ApiServer {
    constructor(opts) {
        super(opts);

        let self = this;
        let log = self._log;

        if (opts.settings == null) throw new Error('Parameter `settings` is missing!');
        if (opts.variables == null) throw new Error('Parameter `variables` is missing!');

        // let settings = opts.settings;
        let variables = opts.variables;

        // configure the server
        let app = self._app;

        app.set('views', path.join(__dirname, '../../', 'static/views/'));
        app.set('view engine', 'ejs');

        let ejsRender = function (page, opts) {
            return function (req, res) {
                let pageOpts = Object.assign(
                    opts
                );
                res.render(page, pageOpts);
            }
        }

        let renderUtils = new RenderUtils({
            log: log
        })

        let pageOpts = Object.assign({},
            { utils: renderUtils },
            variables
        )
        app.get('/', ejsRender('index', pageOpts));
        app.get('/index.html', ejsRender('index', pageOpts));

        // JavaScript and CSS files
        // app.use('/lib', express.static(path.join(__dirname, '../../static/public/lib')));
        app.use('/lib', express.static(path.join(__dirname, '../../static/public/lib')));
        app.use('/img', express.static(path.join(__dirname, '../../static/public/img')));
        app.use('/js', express.static(path.join(__dirname, '../../static/public/js')));
        app.use('/css', express.static(path.join(__dirname, '../../static/public/css')));
    }

    _getProperties(callback) {
        let self = this;
        let properties = self._propertyManager;

        properties.getProperties({}, callback);
    }
}

exports.ApiServer = ApiServer;
exports.StaticAndApiServer = StaticAndApiServer;
