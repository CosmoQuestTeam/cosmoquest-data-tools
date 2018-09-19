import {wampClient} from './wamp_client';

import { actions } from './store';

import config from './config.json';


// Annotation Libraries

function listAnnotationLibraries() {
    const args = [];

    function onListAnnotationLibraries(success, response) {
        console.log(success, response);

        if (response.annotation_libraries !== undefined) {
            actions.setAnnotationLibraries(response.annotation_libraries);
        }
    }

    wampClient.execute("callRPC", config.crossbar.realm + ".list_annotation_libraries", args, onListAnnotationLibraries);
}


function clearAnnotationLibraries() {
    actions.clearAnnotationLibraries();
}


function refreshAnnotationLibraries() {
    clearAnnotationLibraries();
    listAnnotationLibraries();
}


export {
    listAnnotationLibraries,
    clearAnnotationLibraries,
    refreshAnnotationLibraries
}
