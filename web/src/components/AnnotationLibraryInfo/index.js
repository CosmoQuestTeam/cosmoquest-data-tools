import React, { Component } from 'react';
import PropTypes from 'prop-types';

import { Callout, H2 } from "@blueprintjs/core";


class AnnotationLibraryInfo extends Component {
    constructor(props, context) {
        super(props, context);

        this.state = {};
    }

    static propTypes = {
        annotationLibrary: PropTypes.object.isRequired,
    };

    static defaultProps = {

    };

    componentDidMount() {

    };

    componentWillUnmount() {

    };

    render() {
        return (
            <div className="col-md-12">
                <H2>Information</H2>

                <Callout intent="primary" icon="" style={{ width: "100%", marginBottom: 20}}>
                    <table className="bp3-html-table bp3-condensed bp3-html-table-striped" style={{ width: "95%" }}>
                        <tbody>
                            <tr>
                                <td style={{ boxShadow: "none"}}><strong>Name</strong></td>
                                <td style={{ boxShadow: "none"}}>{this.props.annotationLibrary.name}</td>
                            </tr>
                            <tr>
                                <td><strong>File Path</strong></td>
                                <td>{this.props.annotationLibrary.file_path}</td>
                            </tr>
                            <tr>
                                <td><strong>File Size</strong></td>
                                <td>{this.props.annotationLibrary.file_size}</td>
                            </tr>
                            <tr>
                                <td><strong>Entries</strong></td>
                                <td>{this.props.annotationLibrary.entry_count}</td>
                            </tr>
                            <tr>
                                <td><strong>Annotation Classes</strong></td>
                                <td>{this.props.annotationLibrary.annotation_classes.join(", ")}</td>
                            </tr>
                        </tbody>
                    </table>
                </Callout>
            </div>
        )
    }
}

export default AnnotationLibraryInfo;