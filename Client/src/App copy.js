import React, { Component } from 'react';
import Textbox from './component/textbox';
import axios from 'axios';
import MessageBox from './component/messagebox';
import './App.css';

class App extends Component {

    constructor(){
        super();
    
        console.log("sss");
        this.handleNewUserMessage = this.handleNewUserMessage.bind(this);
        this.state = {
            messages: [
                {
                    type: 1,
                    text: "Hi there. Today we would like to discuss this sentence: 'Al Gore and I are committed to continuing this acquisition program, transforming the military. There's still fewer people in uniform today, but person - to - person, person - by - person, unit - by - unit, this is the most powerful and effective military, not only in the world today, but in the history of the world. And again, Al Gore and I will do whatever is necessary to keep it that way.' I will first decompose the sentence using toulmin's model, and you will argue with me such that you believe the sentence is logically valid."
                }
            ]
        }
    }

    componentDidMount() {
        // Simulate the first interaction with the chatbot
        axios.post('http://127.0.0.1:5000/k', {})
          .then(response => {
            console.log('Initial response: ', response.data);
            this.setState({
              messages: [
                ...this.state.messages,
                {
                  text: response.data,  // Initial response from the chatbot
                  type: 1,  // Type 1 for chatbot's reply
                }
              ]
            });
          })
          .catch(error => {
            console.log(error);
          });
      }

    handleNewUserMessage(text) {
        this.setState({
            messages: this.state.messages.concat([{
                text: text[0].text,
                type: 0,
            }])
        });
        let temp = {
            msg: text[0].text
        };
        console.log('temp: ',temp);
        axios.post('http://127.0.0.1:5000/getReply',{temp})
            .then(res =>{
                console.log('res.data: ',res.data);
                this.setState({
                    messages: this.state.messages.concat([{
                        text: res.data,
                        type: 1,
                    }])
                });
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    countWords(text){
        return text.trim() === "" ? 0 : text.trim().split(/\s+/).length;
    };

    render() {
    return (
      <div className="App">
          <div className="messageBox">
            <MessageBox messageContent={this.state.messages}/>
          </div>
          <Textbox handlerFromParant={this.handleNewUserMessage}/>
      </div>
    );
  }
}

export default App;
