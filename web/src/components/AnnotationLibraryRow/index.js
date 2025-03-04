import React, { Component } from 'react';
import PropTypes from 'prop-types';

import { withRouter } from 'react-router'

import { Button } from "@blueprintjs/core";


class AnnotationLibraryRow extends Component {
    constructor(props, context) {
        super(props, context);

        this.state = {};
    }

    static propTypes = {
        annotationLibrary: PropTypes.object.isRequired,
    };

    static defaultProps = {

    }

    componentDidMount() {

    };

    componentWillUnmount() {

    };

    render() {
        return (
            <tr>
                <td>{this.props.annotationLibrary.name}</td>
                <td><span>{this.props.annotationLibrary.file_path}</span></td>
                <td><span>{this.props.annotationLibrary.file_size}</span></td>
                <td><span>{this.props.annotationLibrary.entry_count}</span></td>
                <td><span>{this.props.annotationLibrary.annotation_classes.join(", ")}</span></td>
                <td style={{padding: "0 11px"}}>
                    <Button 
                        icon="eye-open" 
                        intent="primary" 
                        small 
                        style={{marginTop: 8}}
                        onClick={this.handleInspectClick}
                    >
                        Inspect
                    </Button>
                </td>
            </tr>
        )
    }

    handleInspectClick = (e) => {
        this.props.history.push("annotation_library/" + this.props.annotationLibrary.name);
    }
}

export default withRouter(AnnotationLibraryRow);