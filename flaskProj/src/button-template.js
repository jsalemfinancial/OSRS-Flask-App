import React from 'react';

const FormButton = ({name, onClick}) =>
{
  return (
    <button className="btn btn-warning" onClick={onClick}>{name}</button>
  );
}

export default FormButton;