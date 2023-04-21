import React from 'react';
import {createRoot} from 'react-dom/client';
import LoginRegister from './form-button-component';
import ReactSample from './sample-component';

const formSubmitRoot = document.getElementById("data-placeholder");
const formSubmitComponent = createRoot(formSubmitRoot);

const sampleRoot = document.getElementById("sample-component");
const sampleComponent = createRoot(sampleRoot);

formSubmitComponent.render(<LoginRegister name={"Login/Register"}/>);
sampleComponent.render(<ReactSample/>);