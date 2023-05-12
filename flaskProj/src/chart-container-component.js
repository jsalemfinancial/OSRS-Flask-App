import React from "react";
import FormButton from "./button-template";

class LoginRegister extends React.Component {
    constructor(props)
    {
      super(props);
  
      this.state = {
        data: null
      };
  
      this.handleClick = this.handleClick.bind(this);
    }
  
    handleClick()
    {
      fetch(this.props.endpoint)
          .then(response => response.json())
          .then(data =>
            {
              if (data["response"])
              {
                return alert(data["response"]);
              }
  
              return this.setState({ data })
            });
    }
  
    render()
    {
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