import React, { Component } from 'react';
import PropTypes from 'prop-types';

import { Route } from 'react-router-dom';

import { Icon, Tabs, Tab } from "@blueprintjs/core";

import AnnotationLibraries from '../AnnotationLibraries';

import { Provider } from '../../store';

import './index.css';


class App extends Component {
    constructor(props, context) {
        super(props, context);

        this.state = {};
    }

    componentDidMount() {

    };

    componentWillUnmount() {

    };

    render() {
        return (
            <Provider>
                <div className="row no-gutters" style={{height: "100%"}}>
                    <div className="app col-md-12" style={{height: "100%"}}>
                        <div className="container-fluid" style={{height: "100%"}}>
                            <div className="row" style={{height: "100%"}}>
                                <div className="main col-md-10" style={{height: "100%"}}>
                                    <h1>Cosmoquest Data Tools</h1>

                                    <div className="container-fluid">
                                        <Route path="/" component={AnnotationLibraries} exact />
                                        <Route path="/annotation_libraries" component={AnnotationLibraries} exact />
                                        <Route path="/empty" component={""} exact />
                                    </div>
                                </div>

                                <div className="side col-md-2" style={{height: "100%"}}>
                                    <h2>
                                        <Icon icon="manual" iconSize={20} style={{verticalAlign: -1}}/>
                                        &nbsp;
                                        Navigation
                                    </h2>

                                    <Tabs id="NavigationTabs" onChange={this.handleNavigationClick} vertical>
                                        <Tab id="annotation_libraries" title="Annotation Libraries" />
                                        <Tab id="empty" title="Empty" />
                                    </Tabs>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </Provider>
        )
    }

    handleNavigationClick = (route) => {
        this.props.history.push(route);
    }
}

export default App;
