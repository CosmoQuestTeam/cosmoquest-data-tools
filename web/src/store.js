import createStore from 'react-waterfall';

const config = {
    initialState: {
        annotationLibraries: null
    },
    actionsCreators: {
        setAnnotationLibraries: ({ annotationLibraries }, func, data) => {
            return {
                annotationLibraries: data
            };
        },
        clearAnnotationLibraries: ({ annotationLibraries }) => ({ annotationLibraries: null })
    },
};

export const { Provider, connect, actions } = createStore(config);