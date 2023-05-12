import React from 'react';
import {createRoot} from 'react-dom/client';
import LoginRegister from './chart-container-component';

const formSubmitRoot = document.getElementById("data-placeholder");
const formSubmitComponent = createRoot(formSubmitRoot);

formSubmitComponent.render(<LoginRegister name={"Login/Register"} endpoint={"/data"}/>);