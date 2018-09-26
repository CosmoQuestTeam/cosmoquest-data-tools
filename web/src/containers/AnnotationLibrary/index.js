import React, { Component } from 'react';
import PropTypes from 'prop-types';

import { withRouter } from 'react-router';

import { Spinner, Button } from '@blueprintjs/core';
import { Select } from "@blueprintjs/select";

import AnnotationLibraryInfo from '../../components/AnnotationLibraryInfo';
import BoundingBoxTable from '../../components/BoundingBoxTable';
import ImageViewer from '../../components/ImageViewer';

import './index.css';

import * as AppActions from '../../actions';

import { connect } from '../../store';



class AnnotationLibrary extends Component {
    constructor(props, context) {
        super(props, context);

        this.state = {
            entryIndex: 0
        };
    }

    static propTypes = {
        annotationLibrary: PropTypes.object,
        annotationLibraryEntry: PropTypes.object,
        boundingBoxMetaColors: PropTypes.object
    };

    static defaultProps = {

    }

    componentDidMount() {
        AppActions.getAnnotationLibrary(this.props.match.params.name);
    };

    componentWillUnmount() {
        AppActions.clearAnnotationLibrary();
    };

    render() {
        return (
            <div className="annotation-library col-md-12">
                {(this.props.annotationLibrary === null || this.props.annotationLibraryEntry === null) ? this.renderSkeleton() : this.renderData()}
            </div>
        )
    }

    renderSkeleton = () => {
        return (
            <div>
                <h2>
                    Annotation Library: {this.props.match.params.name}
                    &nbsp;
                    <Spinner className="spinner" size={20} tagName="span" />
                </h2>

                <div className="row align-items-center" style={{ paddingTop: "38vh", textAlign: "center"}}>
                    <div className="col" style={{ fontSize: 48, fontWeight: 700 }}>
                        Loading Annotation Library...
                    </div>
                </div>
            </div>
        )
    }

    renderData = () => {
        return (
            <div>
                <h2>
                    Annotation Library: {this.props.annotationLibrary.name}
                </h2>

                <div className="row">
                    <div className="col-md-8 image-viewer">
                        <canvas id="image_viewer" />

                        <ImageViewer 
                            imageBase64={this.props.annotationLibraryEntry.image_base64}
                            imageWidth={this.props.annotationLibraryEntry.image_width}
                            imageHeight={this.props.annotationLibraryEntry.image_height}
                            boundingBoxes={this.props.annotationLibraryEntry.bounding_boxes}
                            boundingBoxMetaColors={this.props.boundingBoxMetaColors}
                        />
                    </div>

                    <div className="col-md-4">
                        <div className="row">
                            <AnnotationLibraryInfo annotationLibrary={this.props.annotationLibrary} />
                            <BoundingBoxTable 
                                boundingBoxes={this.props.annotationLibraryEntry.bounding_boxes} 
                                boundingBoxMetaColors={this.props.boundingBoxMetaColors}    
                            />
                        </div>
                    </div>
                </div>
            </div>
        )
    }

    renderEntry = (entry) => {
        return (
            <div>{entry}</div>
        )
    }
}

export default withRouter(
    connect(
        ({ 
            annotationLibrary, 
            annotationLibraryEntry,
            boundingBoxMetaColors
        }) => ({ 
            annotationLibrary, 
            annotationLibraryEntry,
            boundingBoxMetaColors
        })
    )(AnnotationLibrary)
)
