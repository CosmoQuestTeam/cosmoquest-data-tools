import React, { Component } from 'react';
import PropTypes from 'prop-types';

import { Route } from 'react-router-dom';

import './index.css';

import * as AppActions from '../../actions/app_actions';


class App extends Component {
    constructor(props, context) {
        super(props, context);

        this.state = {};
    }

    componentDidMount() {
        AppActions.listAnnotationLibraries();
    };

    componentWillUnmount() {

    };

    render() {
        return (
            <div className="app col-md-12">
                <h1>Cosmoquest Data Tools</h1>
            </div>
        )
    }
}

export default App;
