import React from 'react';
import {createRoot} from 'react-dom/client';
import LoginRegister from './chart-container-component';
import { Tooltip, Toast, Popover } from 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

const formSubmitRoot = document.getElementById("data-placeholder");
const formSubmitComponent = createRoot(formSubmitRoot);

formSubmitComponent.render(<LoginRegister name={"Login/Register"} endpoint={"/data"}/>);