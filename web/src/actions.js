import {wampClient} from './wamp_client';

import { Toaster, Position, Intent } from '@blueprintjs/core';

import { actions } from './store';

import config from './config.json';



// Notifications
const Notifier = Toaster.create({
    className: "notifications",
    position: Position.BOTTOM_LEFT
});


function notify(intent, message) {
    Notifier.show({ message, intent, className: "bp3-dark" });
}


function notifyInfo(message) {
    notify(Intent.PRIMARY, message);
}


function notifySuccess(message) {
    notify(Intent.SUCCESS, message);
}


function notifyError(message) {
    notify(Intent.DANGER, message);
}


// Annotation Libraries
function listAnnotationLibraries() {
    const args = [];

    function onListAnnotationLibraries(success, response) {
        if (!success) {
            notifyError("An error occurred...");
            return;
        }

        if (success && !response.success[0]) {
            notifyError(response.success[1]);
            return;
        }

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


// Annotation library

function getAnnotationLibrary(name) {
    const args = [name];

    function onGetAnnotationLibrary(success, response) {
        if (!success) {
            notifyError("An error occurred...");
            return;
        }

        if (success && !response.success[0]) {
            notifyError(response.success[1]);
            return;
        }

        if (response.annotation_library !== null) {
            actions.setAnnotationLibrary(response.annotation_library);
            actions.setAnnotationLibraryEntry(response.annotation_library.annotation_library_entry);
        }
    }

    wampClient.execute("callRPC", config.crossbar.realm + ".get_annotation_library", args, onGetAnnotationLibrary);
}


function clearAnnotationLibrary() {
    actions.clearAnnotationLibrary();
}


function getAnnotationLibraryEntry(name, index) {
    const args = [name, index];

    function onGetAnnotationLibraryEntry(success, response) {
        if (!success) {
            notifyError("An error occurred...");
            return;
        }

        if (success && !response.success[0]) {
            notifyError(response.success[1]);
            return;
        }

        if (response.annotation_library_entry !== null) {
            actions.setAnnotationLibraryEntry(response.annotation_library_entry);
        }
    }

    wampClient.execute("callRPC", config.crossbar.realm + ".get_annotation_library_entry", args, onGetAnnotationLibraryEntry);
}


function clearAnnotationLibraryEntry() {
    actions.clearAnnotationLibraryEntry();
}


export {
    notifyInfo,
    notifySuccess,
    notifyError,
    listAnnotationLibraries,
    clearAnnotationLibraries,
    refreshAnnotationLibraries,
    getAnnotationLibrary,
    clearAnnotationLibrary,
    getAnnotationLibraryEntry,
    clearAnnotationLibraryEntry
}
