let dmoz = require('dmoz');
let args = require('minimist')(process.argv.slice(2));

if (args.rdf == null) throw new Error('Parameter `rdf` missing!');
if (args.bow == null) throw new Error('Parameter `bow` missing!');
if (args.bowPart == null) throw new Error('Parameter `bowPart` missing!');

let dirnameIn = args.rdf;
let bowFName = args.bow;
let bowPartFName = args.bowPart;

dmoz.construct({
    rdfPath: dirnameIn,
    bow: bowFName,
    bowPart: bowPartFName,
    categoryMinSize: 100
})
