import createStore from 'react-waterfall';

import colorbrewer from 'colorbrewer';

const colorPalette = colorbrewer.Set1[9];

const config = {
    initialState: {
        annotationLibraries: null,
        annotationLibrary: null,
        annotationLibraryEntry: null,
        boundingBoxMetaColors: {},
        boundingBoxMetaColorPaletteIndex: 0,
        selectedBoundingBoxIndex: null
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
        setAnnotationLibraryEntry: ({ annotationLibraryEntry, boundingBoxMetaColors, boundingBoxMetaColorPaletteIndex }, func, data) => {
            data.bounding_boxes.forEach((bb, i) => {
                if (boundingBoxMetaColors[bb.meta] === undefined) {
                    boundingBoxMetaColors[bb.meta] = colorPalette[boundingBoxMetaColorPaletteIndex];
                    boundingBoxMetaColorPaletteIndex += 1;

                    if (boundingBoxMetaColorPaletteIndex > 8) {
                        boundingBoxMetaColorPaletteIndex = 0;
                    }
                }
            });

            return {
                annotationLibraryEntry: data,
                boundingBoxMetaColors,
                boundingBoxMetaColorPaletteIndex
            };
        },
        clearAnnotationLibraryEntry: ({ annotationLibraryEntry }) => ({ annotationLibraryEntry: null }),
        setSelectedBoundingBoxIndex: ({ selectedBoundingBoxIndex }, func, data) => {
            return {
                selectedBoundingBoxIndex: data
            };
        },
    },
};

export const { Provider, connect, actions } = createStore(config);