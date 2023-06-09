import React from 'react';
import {createRoot} from 'react-dom/client';
import TestData from './form-button-component';
import Population from './pagination-component';
import { Tooltip, Toast, Popover } from 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

const formSubmitRoot = document.getElementById("data-placeholder");
const formSubmitComponent = createRoot(formSubmitRoot);

class App extends React.Component {
    render() {
        return (
            <div id="main-components-container">
                <TestData name={"Show Data"} endpoint={"/data"}/>
                <br/>
                <Population name={"Paginated Data"} endpoint={"/popular"}/>
            </div>
        );
    }
}

formSubmitComponent.render(<App/>);
