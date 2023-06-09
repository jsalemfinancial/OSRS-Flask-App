import React from 'react';
import FormButton from './button-template';

const TestData = ({name, endpoint}) => {
  const [data, setData] = React.useState({});

  const handleClick = () =>
  {
    fetch(endpoint)
        .then(response => response.json())
        .then(data => setData(data));
  }

  if (Object.keys(data) == 0 || "notLogged" in data) {
    return (
      <div>
        <FormButton onClick={handleClick} name={name}/>
      </div>
    );
  }

  return (
      <div>
          <p>Name: {data.name}</p>
          <p>Pronouns: {data.pronouns}</p>
      </div>
  );
}

export default TestData;