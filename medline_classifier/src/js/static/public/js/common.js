var App = {};

//====================================
// COMMUNICATION WITH BACKEND
//====================================

App.Api = {};

App.Api._post = function (url, data, callback) {
    $.ajax({
        url: url,
        type: 'POST',
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: 'json',
        success: function (result) {
            callback(undefined, result);
        },
        error: function (xhr, textStatus, e) {
            if (xhr.responseJSON != null) {
                var res = xhr.responseJSON;
                callback(new Error(res.message));
            } else {
                callback(new Error(e));
            }
        }
    });
}

App.Api.sendRequest = function (method, params, callback) {
    App.Api._post('api/' + method, params, callback);
}

//====================================
// EXECUTORS
//====================================

App.Executors = {};

App.Executors.series = function (tasks, callback) {
    var nTasks = tasks.length;
    var results = [];
    for (var taskN = 0; taskN < nTasks; ++taskN) {
        results.push(null);
    }

    var currTaskN = 0;
    var callbackCalled = false;

    var finish = function (e) {
        if (!callbackCalled) {
            if (e != null) {
                console.error(e);
            }
            callbackCalled = true;
            callback(e, results);
        }
    }

    var executeNext = function () {
        if (currTaskN >= nTasks) {
            finish();
        } else {
            var task = tasks[currTaskN];

            try {
                task(function (e, result) {
                    if (e != null) return finish(e);

                    results[currTaskN] = result;

                    ++currTaskN;
                    executeNext();
                })
            } catch (e) {
                finish(e);
            }
        }
    }

    executeNext();
}

App.Executors.parallel = function (tasks, callback) {
    var nTasks = tasks.length;
    var results = [];

    for (var resultN = 0; resultN < nTasks; ++resultN) {
        results.push(null);
    }

    var finishedTaskN = 0;
    var callbackCalled = false;

    var finish = function (e) {
        if (!callbackCalled) {
            if (e != null) {
                console.error(e);
            }
            callbackCalled = true;
            callback(e, results);
        }
    }

    var executeTask = function (taskN) {
        var task = tasks[taskN];

        try {
            task(function (e, result) {
                if (e != null) return finish(e);

                results[taskN] = result;
                ++finishedTaskN;

                if (finishedTaskN >= nTasks) {
                    finish();
                }
            })
        } catch (e) {
            finish(e);
        }
    }

    for (var taskN = 0; taskN < nTasks; ++taskN) {
        executeTask(taskN);
    }
}

App.Executors.executeAfterIdle = function (delay, callback) {
    var state = {
        timeoutId: null,
        touchTime: null
    }

    return {
        touch: function () {
            state.touchTime = Date.now();

            if (state.timeoutId == null) {
                var onTimeout = function () {
                    var now = Date.now();
                    var elapsed = now - state.touchTime;
                    var timeLeft = delay - elapsed;

                    if (timeLeft > 0) {
                        state.timeoutId = setTimeout(onTimeout, timeLeft);
                    } else {
                        state.timeoutId = null;
                        state.touchTime = null;
                        callback();
                    }
                }
                state.timeoutId = setTimeout(onTimeout, delay);
            }
        }
    }
}
