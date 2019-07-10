(function () {

    //======================================
    // INDEX MODEL
    //======================================

    var IndexModel = function () {

    }

    IndexModel.prototype.init = function (callback) {
        callback();
    }

    IndexModel.prototype.fetchCategories = function (opts, callback) {
        App.Api.sendRequest('classify', opts, callback);
    }

    //======================================
    // CONTROLLER
    //======================================

    var IndexController = function (opts) {
        var self = this;

        if (opts.model == null) throw new Error('Parameter `model` is missing!');

        self._hideErrorExecutor = App.Executors.executeAfterIdle(10000, function () {
            self._vue.errorMessage = null;
        })

        self._MAX_CATEGORIES = 200;

        self._model = opts.model;
        self._vue = new Vue({
            el: '#page-wrapper',
            data: {
                text: null,
                maxCategories: 10,
                categories: [],
                errorMessage: null
            },
            methods: {
                onFetchCategories: function () {
                    self._fetchCategories();
                },
                clearCategories: function () {
                    self._vue.categories = [];
                },
                formatWeight: function (weight) {
                    return (100*weight).toFixed();
                },
                handleMaxCategoriesChange: function () {
                    var vue = self._vue;
                    var maxCat = parseInt(vue.maxCategories);
                    if (maxCat < 1) { vue.maxCategories = 1; }
                    if (maxCat > self._MAX_CATEGORIES) { vue.maxCategories = self._MAX_CATEGORIES; }
                }
            }
        })
    }

    IndexController.prototype.init = function (callback) {
        callback();
    }

    IndexController.prototype._fetchCategories = function () {
        var self = this;
        var model = self._model;
        var vue = self._vue;

        try {
            var text = vue.text;
            var maxCategories = parseInt(vue.maxCategories);

            if (text == null || text.length < 32) {
                throw 'The text should be at least 32 characters long!';
            }
            if (isNaN(maxCategories) || maxCategories < 1 || maxCategories > self._MAX_CATEGORIES) {
                throw 'Invalid number of categories!';
            }

            var opts = {
                text: text,
                maxCategories: maxCategories,
            }

            model.fetchCategories(opts, function (e, categories) {
                if (e != null) {
                    self._handleError('Oops, an error occurred! Please contact the administrator!');
                    return;
                }
                vue.categories = categories.map(function (category) {
                    return {
                        category: category.category,
                        weight: category.weight,
                        explanation: category.fullCategories.join('\n')
                    }
                });
            })
        } catch (e) {
            self._handleError(e);
        }
    }

    IndexController.prototype._handleError = function (msg) {
        var self = this;
        var vue = self._vue;

        if (typeof msg != 'string') { msg = msg.message; }

        vue.errorMessage = msg;
        self._hideErrorExecutor.touch();
    }

    //======================================
    // INITIALIZE
    //======================================

    $(document).ready(function () {
        Vue.filter('formatWeight', function (weight) {
            if (typeof weight != 'number') { return weight; }
            return (100*weight).toFixed() + '%';
        })

        var model = new IndexModel();
        var controller = new IndexController({
            model: model
        })

        var phase1 = [
            function (xcb) {
                model.init(xcb);
            },
            function (xcb) {
                controller.init(xcb);
            }
        ]
        App.Executors.series(phase1, function (e) {
            if (e != null) {
                console.error('Exception while initializing the page!');
                console.error(e);
            }

            $('#page-wrapper').removeClass('d-none');
        })
    })
})();
