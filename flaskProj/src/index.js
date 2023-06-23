import React from 'react';
import {createRoot} from 'react-dom/client';
import TestData from './form-button-component';
import { Tooltip, Toast, Popover } from 'bootstrap';
import "../src/custom.scss"

const root = document.getElementById("react-root");
const rootComponent = createRoot(root);

class App extends React.Component {
    render() {
        return (
            <div className="container-fluid bg-primary m-0 p-0">
                <div className="container-fluid bg-secondary">
                    <TestData name={"Show Data"} endpoint={"/data"}/>
                </div>

                <div className="container center-block">
                    <object
                        data="/active/p1.html">
                    </object>
                    
                    <object
                        data="/active/p2.html">
                    </object>

                    <object
                        data="/active/p3.html">
                    </object>

                    <object
                        data="/active/p4.html">
                    </object>

                    <object
                        data="/active/p5.html">
                    </object>

                    <object
                        data="/active/p6.html">
                    </object>
                </div>
            </div>
        );
    }
}

rootComponent.render(<App/>);
