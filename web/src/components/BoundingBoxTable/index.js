import React, { Component } from 'react';
import PropTypes from 'prop-types';

import { Callout, H2, Pre, Tag } from "@blueprintjs/core";


class BoundingBoxTable extends Component {
    constructor(props, context) {
        super(props, context);

        this.state = {};
    }

    static propTypes = {
        boundingBoxes: PropTypes.array.isRequired,
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
                <H2>Bounding Boxes</H2>

                <Callout intent="primary" icon="" style={{ width: "100%", maxHeight: 600, overflowY: "scroll" }}>
                    <table className="bp3-html-table bp3-condensed bp3-html-table-striped" style={{ width: "95%" }}>
                        <thead>
                            <tr>
                                <th style={{ width: 140 }}>(y0, x0, y1, x1)</th>
                                <th>Label</th>
                                <th>Meta</th>
                            </tr>
                        </thead>

                        <tbody>
                            { this.props.boundingBoxes.map((bb, i) => {
                                return (
                                    <tr>
                                        <td><Pre style={{ padding: 5, width: 140 }}>({ bb.y0 },{ bb.x0 },{ bb.y1 },{ bb.x1 })</Pre></td>
                                        <td><Tag icon="edit" style={{ marginTop: 13 }}>{bb.label}</Tag></td>
                                        <td><Tag intent="success" style={{ marginTop: 13 }}>{bb.meta}</Tag></td>
                                    </tr>
                                )
                            })}
                        </tbody>
                    </table>
                </Callout>
            </div>
        )
    }
}

export default BoundingBoxTable;