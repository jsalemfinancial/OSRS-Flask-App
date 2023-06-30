import React from 'react';
import {createRoot} from 'react-dom/client';
import { BrowserRouter, Link, Routes, Route } from 'react-router-dom';
import HeatMap from './heatmap-component';
import { Tooltip, Toast, Popover } from 'bootstrap';
import "../src/custom.scss"

const root = document.getElementById("react-root");
const rootComponent = createRoot(root);

class App extends React.Component {
    render() {
        return (
            <div className="d-xl-flex flex-row bg-primary h-100 m-0 p-0">
                <div className=" d-sm-flex bg-dark">
                    <ul className="nav nav-tabs flex-column p-2 bg-secondary">
                        <li> <Link to="/">Home</Link> </li>
                        <li> <Link to="/messages">Messages</Link> </li>
                        <li> <Link to="/about">About</Link> </li>
                        <li> <Link to="/heatmap">Heatmap</Link> </li>
                    </ul>
                </div>

                <Routes className="d-lg-flex flex-row flex-grow-1 justify-content-lg-center bg-light m-0 p-0">
                    <Route path="/heatmap" Component={HeatMap}/>
                    {/* <div className="d-sm-flex flex-column m-0 bg-dark">
                        <object
                            data="/active/p1.html">
                        </object>
                        
                        <object
                            data="/active/p2.html">
                        </object>

                        <object
                            data="/active/p3.html">
                        </object>
                    </div>

                    <div className="d-sm-flex flex-column m-0 bg-dark">
                        <object
                                data="/active/p4.html">
                            </object>

                            <object
                                data="/active/p5.html">
                            </object>

                            <object
                                data="/active/p6.html">
                        </object>
                    </div> */}
                </Routes>
            </div>
        );
    }
}

rootComponent.render
(
    <BrowserRouter>
        <App/>
    </BrowserRouter>
);
