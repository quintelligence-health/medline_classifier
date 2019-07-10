let dmoz = require('dmoz');
let srv = require('./server/server');
let log = require('./utils/logger');
let args = require('./utils/arguments');

let settings = args.settings;

if (settings.classifier.bow == null) throw new Error('Parameter `bow` missing!');
if (settings.classifier.bowPart == null) throw new Error('Parameter `bowPart` missing!');
if (settings.classifier.classifier == null) throw new Error('Parameter `classifier` missing!');
if (settings.classifier.filter == null) throw new Error('Parameter `filter` missing!');

let blacklist = [
    'Anatomy/Animal Structures',
    'Anatomy/Plant Structures',
    'Analytical, Diagnostic and Therapeutic Techniques and Equipment',
    'Psychiatry and Psychology/Behavior and Behavior Mechanisms',
    'Psychiatry and Psychology/Psychological Phenomena',
    'Phenomena and Processes/Plant Physiological Phenomena',
    'Phenomena and Processes/Mathematical Concepts',
    'Disciplines and Occupations',
    'Anthropology, Education, Sociology and Social Phenomena',
    'Technology, Industry, Agriculture/Technology, Industry, and Agriculture',
    'Technology, Industry, Agriculture/Non-Medical Public and Private Facilities',
    'Humanities',
    'Information Science',
    'Named Groups',
    'Health Care',
    'Publication Characteristics',
    'Geographicals'
]


function initializeClassifier(params, callback) {
    try {
        log.info('initializing classifier');
        let classifier = new dmoz.Classifier(params, blacklist);
        callback(undefined, classifier);
    } catch (e) {
        callback(e);
    }
}

let classifierParam = {
    bow: settings.classifier.bow,
    bowPart: settings.classifier.bowPart,
    classifier: settings.classifier.classifier,
    filter: settings.classifier.filter,
    blacklist: blacklist
}

initializeClassifier(classifierParam, function (e, classifier) {
    if (e != null) {
        log.error(e, 'Failed to initialize the classifier!');
        process.exit(1);
    }

    if (args.port != null) {
        settings.server.port = args.port;
    }

    log.info('initializing the server');
    let server = new srv.StaticAndApiServer({
        settings: settings.server,
        variables: {},
        log: log
    })

    server.initApi('api');

    server.on('api', 'classify', function (params, callback) {
        log.info('classifying');

        let text = params.text;
        let maxCategories = params.maxCategories != null ?
                params.maxCategories : 20;
        let cutoffSimilarity = params.cutoffSimilarity != null ?
                params.cutoffSimilarity : 0.0;

        let result = classifier.classify(text, maxCategories, cutoffSimilarity);
        callback(undefined, result);
    })

    server.init(function (e) {
        if (e != null) {
            log.error(e, 'Failed to initialize the server!');
            process.exit(2);
        }

        log.info('server initialized!');
    })


//     app.post('/classify', function (req, res) {
//         log.info('classifying');

//         let handleError = function (e) {
//             console.error(e);
//             res.status(500);    // internal server error
//             res.send(e.message);
//             res.end();
//         }

//         try {
//             let body = req.body;
//             let text = body.text;
//             let maxCategories = body.maxCategories != null ?
//                     body.maxCategories : 10;

//             let result = classifier.classify(text, maxCategories);
//             res.send(result);
//             res.end();
//         } catch (e) {
//             handleError(e);
//         }
//     })

//     app.listen(args.port);
//     log.info('server listening on port ' + args.port);
})
