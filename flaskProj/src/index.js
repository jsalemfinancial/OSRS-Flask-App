import React from 'react';
import {createRoot} from 'react-dom/client';
import { BrowserRouter, Link, Routes, Route } from 'react-router-dom';
import HeatMap from './heatmap-component';
import ActiveCharts from './active-charts-component';
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
                        <li> <Link to="/about">About</Link> </li>
                        <li> <Link to="/active">Active</Link> </li>
                        <li> <Link to="/heatmap">Heatmap</Link> </li>
                    </ul>
                </div>

                <Routes className="d-lg-flex flex-row flex-grow-1 justify-content-lg-center bg-light m-0 p-0">
                    <Route path="/" element={<div>Need a home page :O</div>}/>
                    <Route path="/about" element={<div>Blah Blah Blah Blahhhhhh</div>}/>
                    <Route path="/active" element={<ActiveCharts moniker={"p"} endpoint={"active"} amount={7}/>}/>
                    <Route path="/heatmap" element={<HeatMap/>}/>
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
