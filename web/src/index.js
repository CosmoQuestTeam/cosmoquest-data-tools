import React from 'react';
import ReactDOM from 'react-dom';

import {BrowserRouter, Route} from 'react-router-dom';

import App from './containers/App';

import {wampClient} from './wamp_client';

import 'normalize.css/normalize.css';

import 'bootstrap/dist/css/bootstrap-grid.css'

import '@blueprintjs/core/lib/css/blueprint.css';
import '@blueprintjs/icons/lib/css/blueprint-icons.css';

import './index.css';

ReactDOM.render(
    <BrowserRouter>
        <div className="bp3-dark" style={{height: "100%"}}>
            <Route path="/" component={App} />
        </div>
    </BrowserRouter>,
    document.getElementById("root")
);