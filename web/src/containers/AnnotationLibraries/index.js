import React, { Component } from 'react';
import PropTypes from 'prop-types';

import { Spinner, NonIdealState, Button} from '@blueprintjs/core';

import AnnotationLibraryRow from '../../components/AnnotationLibraryRow';

import './index.css';

import * as AppActions from '../../actions';

import { connect } from '../../store';


class AnnotationLibraries extends Component {
    constructor(props, context) {
        super(props, context);

        this.state = {

        };
    }

    static propTypes = {
        annotationLibraries: PropTypes.array,
    };

    static defaultProps = {

    }

    componentDidMount() {
        AppActions.listAnnotationLibraries();
    };

    componentWillUnmount() {
        AppActions.clearAnnotationLibraries();
    };

    render() {
        return (
            <div className="annotation-libraries col-md-12">
                {this.props.annotationLibraries === null ? this.renderSkeleton() : ""}
                {(this.props.annotationLibraries !== null && this.props.annotationLibraries.length === 0) ? this.renderNoData() : ""}
                {(this.props.annotationLibraries !== null && this.props.annotationLibraries.length > 0) ? this.renderData() : ""}
            </div>
        )
    }

    renderSkeleton = () => {
        return (
            <div>
                <h2>
                    Annotation Libraries
                    &nbsp;
                    <Spinner className="spinner" size={20} tagName="span"/>
                </h2>

                <table className="bp3-html-table bp3-interactive" style={{width: "100%"}}>
                    <thead>
                        <tr>
                            <th><span className="bp3-skeleton">Name</span></th>
                            <th><span className="bp3-skeleton">File Path</span></th>
                            <th><span className="bp3-skeleton">File Size</span></th>
                            <th><span className="bp3-skeleton">Entries</span></th>
                            <th><span className="bp3-skeleton">Annotation Classes</span></th>
                            <th><span className="bp3-skeleton"></span></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><span className="bp3-skeleton">annotation_library</span></td>
                            <td><span className="bp3-skeleton">data/annotation_library.alh5</span></td>
                            <td><span className="bp3-skeleton">9 GB</span></td>
                            <td><span className="bp3-skeleton">10000</span></td>
                            <td><span className="bp3-skeleton">Crater</span></td>
                            <td><span className="bp3-skeleton"></span></td>
                        </tr>
                        <tr>
                            <td><span className="bp3-skeleton">annotation_library</span></td>
                            <td><span className="bp3-skeleton">data/annotation_library.alh5</span></td>
                            <td><span className="bp3-skeleton">9 GB</span></td>
                            <td><span className="bp3-skeleton">10000</span></td>
                            <td><span className="bp3-skeleton">Crater</span></td>
                            <td><span className="bp3-skeleton"></span></td>
                        </tr>
                        <tr>
                            <td><span className="bp3-skeleton">annotation_library</span></td>
                            <td><span className="bp3-skeleton">data/annotation_library.alh5</span></td>
                            <td><span className="bp3-skeleton">9 GB</span></td>
                            <td><span className="bp3-skeleton">10000</span></td>
                            <td><span className="bp3-skeleton">Crater</span></td>
                            <td><span className="bp3-skeleton"></span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        )
    }

    renderNoData = () => {
        return (
            <div>
                <h2 style={{marginBottom: 80}}>
                    Annotation Libraries
                </h2>

                <NonIdealState
                    icon="search"
                    title="No Annotation Libraries Found"
                    description="Couldn't find any annotation libraries in your /data directory."
                    action={<Button intent="success" icon="new-object" onClick={this.handleNewAnnotationLibraryClick}>Create a new Annotation Library</Button>}
                />
            </div>
        )
    }

    renderData = () => {
        return (
            <div>
                <h2>
                    Annotation Libraries ({this.props.annotationLibraries.length * 3})
                </h2>

                <table className="bp3-html-table bp3-interactive" style={{width: "100%"}}>
                    <thead>
                        <tr style={{fontSize: 16}}>
                            <th><span>Name</span></th>
                            <th><span>File Path</span></th>
                            <th><span>File Size</span></th>
                            <th><span>Entries</span></th>
                            <th><span>Annotation Classes</span></th>
                            <th><span></span></th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.props.annotationLibraries.map((al, i) => {
                            return <AnnotationLibraryRow key={"al-" + i} annotationLibrary={al} />
                        })}
                        {this.props.annotationLibraries.map((al, i) => {
                            return <AnnotationLibraryRow key={"al-" + i} annotationLibrary={al} />
                        })}
                        {this.props.annotationLibraries.map((al, i) => {
                            return <AnnotationLibraryRow key={"al-" + i} annotationLibrary={al} />
                        })}
                    </tbody>
                </table>

                <div className="row" style={{ marginTop: 50 }}>
                    <Button 
                        intent="success" 
                        icon="plus" 
                        large 
                        style={{ marginRight: 15 }} 
                        onClick={this.handleNewAnnotationLibraryClick}
                    >
                        Create Annotation Library
                    </Button>

                    <Button 
                        icon="refresh" 
                        large 
                        onClick={this.handleRefreshClick}
                    >
                        Refresh
                    </Button>
                </div>
            </div>
        )
    }

    handleNewAnnotationLibraryClick = (e) => {

    }

    handleRefreshClick = (e) => {
        AppActions.refreshAnnotationLibraries();
    }
}

export default connect(({ annotationLibraries }) => ({ annotationLibraries }))(AnnotationLibraries)
