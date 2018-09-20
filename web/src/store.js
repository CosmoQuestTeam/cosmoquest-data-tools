import createStore from 'react-waterfall';

const config = {
    initialState: {
        annotationLibraries: null,
        annotationLibrary: null,
        annotationLibraryEntry: null
    },
    actionsCreators: {
        setAnnotationLibraries: ({ annotationLibraries }, func, data) => {
            return {
                annotationLibraries: data
            };
        },
        clearAnnotationLibraries: ({ annotationLibraries }) => ({ annotationLibraries: null }),
        setAnnotationLibrary: ({ annotationLibrary }, func, data) => {
            return {
                annotationLibrary: data
            };
        },
        clearAnnotationLibrary: ({ annotationLibrary }) => ({ annotationLibrary: null }),
        setAnnotationLibraryEntry: ({ annotationLibraryEntry }, func, data) => {
            return {
                annotationLibraryEntry: data
            };
        },
        clearAnnotationLibraryEntry: ({ annotationLibraryEntry }) => ({ annotationLibraryEntry: null }),
    },
};

export const { Provider, connect, actions } = createStore(config);