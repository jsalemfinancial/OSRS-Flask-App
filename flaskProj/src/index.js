import React from 'react';
import {createRoot} from 'react-dom/client';
import TestData from './form-button-component';
import { Tooltip, Toast, Popover } from 'bootstrap';
import "../src/custom.scss"

const formSubmitRoot = document.getElementById("data-placeholder");
const formSubmitComponent = createRoot(formSubmitRoot);

class App extends React.Component {
    render() {
        return (
            <>
                <div id="main-components-container">
                    <TestData name={"Show Data"} endpoint={"/data"}/>
                    <br/>
                </div>

                <div style=
                        {{
                            position: "relative",
                            width: 100 + "%",
                            height: 50 + "vh",
                            display: "block",
                            backgroundColor: "beige",
                            display: "flex",
                            flexDirection: "row",
                            overflow: "scroll"
                        }}>
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
            </>
        );
    }
}

formSubmitComponent.render(<App/>);
