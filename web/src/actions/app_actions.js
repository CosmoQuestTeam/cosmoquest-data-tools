import {wampClient} from '../helpers/wamp_client';

import AppDispatcher from '../dispatcher/dispatcher';

import config from '../config.json';


// Annotation Libraries

function listAnnotationLibraries() {
    const args = [];

    function onListAnnotationLibraries(success, response) {
        console.log(success, response);

        if (response.annotation_libraries !== undefined) {
            AppDispatcher.dispatch({
                actionType: "LIST_ANNOTATION_LIBRARIES",
                body: response
            });
        }
    }

    wampClient.execute("callRPC", config.crossbar.realm + ".foo", args, onListAnnotationLibraries);
}


export {
    listAnnotationLibraries
}
