import React from 'react';

const FormButton = ({name, onClick}) =>
{
  return (
    <button onClick={onClick}>{name}</button>
  );
}

export default FormButton;