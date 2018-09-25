import React, { Component } from 'react';
import PropTypes from 'prop-types';

import * as PIXI from "pixi.js";


class ImageViewer extends Component {
    constructor(props, context) {
        super(props, context);

        this.state = {
            x: 0,
            y: 0,
            scaleX: 1.0,
            scaleY: 1.0,
            zooming: {
                inProgress: false,
                remainingFactor: 1,
                lastUpdate: 0,
                epsilon: 0.001
            },
            panning: {

            }
        };

        this.application = null;
        this.applicationRendered = false;
    }

    static propTypes = {
        imageBase64: PropTypes.string,
        boundingBoxes: PropTypes.array
    };

    static defaultProps = {
        boundingBoxes: []
    };

    componentDidMount() {
        this.initializeApplication();
    };

    componentWillUnmount() {

    };

    render() {
        if (this.application !== null) {
            if (!this.applicationRendered) {
                this.resetCanvas();
                this.registerEventHandlers();
                this.renderImage();

                this.applicationRendered = true;
            }
            else {
                this.updateCanvas();
            }

            this.application.renderer.render(this.application.stage);
        }

        return (null);
    }

    resetCanvas = () => {
        this.application.stage.removeChildren();
    }

    updateCanvas = () => {
        this.application.stage.x = this.state.x;
        this.application.stage.y = this.state.y;
        this.application.stage.scale.x = this.state.scaleX;
        this.application.stage.scale.y = this.state.scaleY;
    }

    registerEventHandlers = () => {
        // Mouse Wheel Zoom
        this.application.view.addEventListener("wheel", (e) => {
            const zoomDirection = e.deltaY < 0 ? "IN" : "OUT";
            let zoomFactor;

            if (zoomDirection === "IN") {
                zoomFactor = 1.1;
            }
            else if (zoomDirection === "OUT") {
                zoomFactor = 1 / 1.1;
            }

            this.state.zooming.remainingFactor *= zoomFactor;

            if (!this.state.zooming.inProgress) {
                this.state.zooming.lastUpdate = Date.now();
                this.state.zooming.inProgress = true;
                requestAnimationFrame(this.zoomCanvasSmooth)
            }

            e.preventDefault();
        })
    }

    renderImage = () => {
        let image = new PIXI.Sprite.fromImage("data:image/png;base64," + this.props.imageBase64);

        image.width = this.height; // Assuming square image on a standard display...
        image.height = this.height;

        image.x = (this.width - this.height) / 2;
        image.y = 0;

        this.application.stage.addChild(image);
    }

    initializeApplication = () => {
        // Ironically refs don't work for this and DOM reading does... 
        const container = Array.from(document.getElementsByClassName("image-viewer"))[0];

        this.width = container.clientWidth - 10;
        this.height = container.clientHeight;

        this.application = new PIXI.Application(
            this.width,
            this.height,
            {
                view: document.getElementById("image_viewer"),
                transparent: true
            }
        )

        this.application.stage.interactive = true;

        PIXI.settings.SCALE_MODE = PIXI.SCALE_MODES.NEAREST;

        this.setState(this.state);
    }

    zoomCanvas = (factor) => {
        let newState = {...this.state};

        newState.scaleX *= factor;
        newState.scaleY *= factor;

        const cursorLocation = this.application.renderer.plugins.interaction.eventData.data.global;

        newState.x -= (cursorLocation.x - newState.x) * (factor - 1);
        newState.y -= (cursorLocation.y - newState.y) * (factor - 1);
    
        this.setState(this.sanitizeState(newState));
    }

    zoomCanvasSmooth = () => {
        const time = Date.now();
        const timeDelta = time - this.state.zooming.lastUpdate;

        this.state.zooming.lastUpdate = time;

        const step = Math.pow(this.state.zooming.remainingFactor, timeDelta / 100);
        this.state.zooming.remainingFactor /= step;

        this.zoomCanvas(step);

        if (Math.abs(this.state.zooming.remainingFactor - 1) < this.state.zooming.epsilon) {
            this.zoomCanvas(this.state.zooming.remainingFactor);
            
            this.state.zooming.remainingFactor = 1;
            this.state.zooming.inProgress = false;
        }
        else {
            requestAnimationFrame(this.zoomCanvasSmooth);
        }
    }

    sanitizeState = (newState) => {
        const comboState =  {...this.state, ...newState};

        comboState.x = Math.min(0, comboState.x);
        comboState.y = Math.min(0, comboState.y);

        const visibleWidth = (this.application.renderer.width * comboState.scaleX) + comboState.x;
        
        if (visibleWidth < this.application.view.width) {
            comboState.x = Math.min(0, this.application.view.width - (this.application.renderer.width * comboState.scaleX));
            if (comboState.x === 0) {
                comboState.scaleX = this.application.view.width / this.application.renderer.width;		
            }
        }

        const visibleHeight = (this.application.renderer.height * comboState.scaleY) + comboState.y;

        if (visibleHeight < this.application.view.height) {
            comboState.y = Math.min(0, this.application.view.height - (this.application.renderer.height * comboState.scaleY));

            if (comboState.x === 0) {
                comboState.scaleY = this.application.view.height / this.application.renderer.height;
            }
        }

        if (comboState.scaleY != comboState.scaleX) {
            comboState.scaleX = Math.max(comboState.scaleX, comboState.scaleY);
            comboState.scaleY = Math.max(comboState.scaleX, comboState.scaleY);
        }

        return comboState;
    }
}

export default ImageViewer;