import React from 'react';

class FormButton extends React.Component {
  render() {
    return (
      <button onClick={this.props.onClick}>{this.props.name}</button>
    );
  }
}

class LoginRegister extends React.Component {
  constructor(props) {
    super(props);
    
    this.state = {
      data: null
    };

    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    fetch('/data')
        .then(response => response.json())
        .then(data => this.setState({ data }));
  }

  render() {
    const { data } = this.state;

    if (!data) {
      return (
        <span>
          <FormButton onClick={this.handleClick} name={this.props.name}/>
        </span>
      );
    }

    return (
        <span>
            <p>Name: {data.name}</p>
            <p>Pronouns: {data.pronouns}</p>
        </span>
    );
  }
}

export default LoginRegister;