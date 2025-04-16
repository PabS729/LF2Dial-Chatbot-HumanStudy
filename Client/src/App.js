import React, { Component } from 'react';
import Textbox from './component/textbox';
import axios from 'axios';
import MessageBox from './component/messagebox';
import './App.css';

class App extends Component {
  constructor() {
    super();

    console.log("sss");
    this.handleNewUserMessage = this.handleNewUserMessage.bind(this);
    this.handleSessionChange = this.handleSessionChange.bind(this);
    this.createNewSession = this.createNewSession.bind(this);
    
    this.state = {
      sessions: [
        {
          id: 1,
          name: "Chatbot1",
          messages: [
            {
              type: 1,
              text: "Hi there. Today we would like to discuss this sentence: 'Al Gore and I are committed to continuing this acquisition program, transforming the military. There's still fewer people in uniform today, but person - to - person, person - by - person, unit - by - unit, this is the most powerful and effective military, not only in the world today, but in the history of the world. And again, Al Gore and I will do whatever is necessary to keep it that way.' I will first decompose the sentence using toulmin's model, and you will argue with me such that you believe the sentence is logically valid."
            }
          ]
        },

        {
            id: 2,
            name: "Chatbot2",
            messages: [
              {
                type: 1,
                text: "Hi there. Today we would like to discuss this sentence: 'Al Gore and I are committed to continuing this acquisition program, transforming the military. There's still fewer people in uniform today, but person - to - person, person - by - person, unit - by - unit, this is the most powerful and effective military, not only in the world today, but in the history of the world. And again, Al Gore and I will do whatever is necessary to keep it that way.' I will first decompose the sentence using toulmin's model, and you will argue with me such that you believe the sentence is logically valid."
              }
            ]
        }


      ],
      currentSessionId: 1,
      nextSessionId: 3
    };
  }

  componentDidMount() {
    // Initialize both sessions with initial messages from the server
    this.initializeSession(1);
    this.initializeSession(2);
  }

  initializeSession(sessionId) {
    var link;
    if (sessionId === 1) {
        link = 'http://127.0.0.1:5000/k';
    }
    else {
        link = 'http://127.0.0.1:5000/s';
    }
    axios.post(link, { sessionId })
      .then(response => {
        console.log(`Session ${sessionId} initial response: `, response.data);
        
        this.setState(prevState => {
          const updatedSessions = [...prevState.sessions];
          const sessionIndex = updatedSessions.findIndex(session => session.id === sessionId);
          
        updatedSessions[sessionIndex].messages.push({
                text: response.data,
                type: 1
              });

          return {
            sessions: updatedSessions
          };
        });
      })
      .catch(error => {
        console.log(`Error initializing session ${sessionId}:`, error);
      });
  }


  handleNewUserMessage(text) {
    const updatedSessions = [...this.state.sessions];
    const currentSessionIndex = updatedSessions.findIndex(session => session.id === this.state.currentSessionId);
    var link = "";
    if (currentSessionIndex !== -1) {
      updatedSessions[currentSessionIndex].messages.push({
        text: text[0].text,
        type: 0
      });
      
      this.setState({
        sessions: updatedSessions
      });
      
      let temp = {
        msg: text[0].text,
        sessionId: this.state.currentSessionId
      };
      
      console.log('temp: ', temp);
      if (currentSessionIndex === 0) {
        link = 'http://127.0.0.1:5000/getReply'
      }
      else {
        link = 'http://127.0.0.1:5000/getReply-Base'
      }
      
      axios.post(link, { temp })
        .then(res => {
          console.log('res.data: ', res.data);
          
          const updatedSessionsAfterReply = [...this.state.sessions];
          const currentSessionIndexAfterReply = updatedSessionsAfterReply.findIndex(
            session => session.id === this.state.currentSessionId
          );
          
          if (currentSessionIndexAfterReply !== -1) {
            updatedSessionsAfterReply[currentSessionIndexAfterReply].messages.push({
              text: res.data,
              type: 1
            });
            
            this.setState({
              sessions: updatedSessionsAfterReply
            });
          }
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  }

  handleSessionChange(event) {
    const sessionId = parseInt(event.target.value, 10);
    this.setState({
      currentSessionId: sessionId
    });
  }

  createNewSession() {
    const newSessionId = this.state.nextSessionId;
    const newSession = {
      id: newSessionId,
      name: `Session ${newSessionId}`,
      messages: []
    };
    
    this.setState(prevState => ({
      sessions: [...prevState.sessions, newSession],
      currentSessionId: newSessionId,
      nextSessionId: prevState.nextSessionId + 1
    }));
    
    // Initialize the new session with a greeting from the chatbot
    axios.post('http://127.0.0.1:5000/k', { sessionId: newSessionId })
      .then(response => {
        console.log('New session initial response: ', response.data);
        
        this.setState(prevState => {
          const updatedSessions = [...prevState.sessions];
          const newSessionIndex = updatedSessions.findIndex(session => session.id === newSessionId);
          
          if (newSessionIndex !== -1) {
            updatedSessions[newSessionIndex].messages.push({
              text: response.data,
              type: 1
            });
          }
          
          return {
            sessions: updatedSessions
          };
        });
      })
      .catch(error => {
        console.log(error);
      });
  }

  countWords(text) {
    return text.trim() === "" ? 0 : text.trim().split(/\s+/).length;
  }

  getCurrentSessionMessages() {
    const currentSession = this.state.sessions.find(session => session.id === this.state.currentSessionId);
    return currentSession ? currentSession.messages : [];
  }

  render() {
    const currentMessages = this.getCurrentSessionMessages();
    
    return (
      <div className="App">
        <div className="session-controls">
          <select 
            value={this.state.currentSessionId} 
            onChange={this.handleSessionChange}
            className="session-selector"
          >
            {this.state.sessions.map(session => (
              <option key={session.id} value={session.id}>
                {session.name}
              </option>
            ))}
          </select>
          <button 
            onClick={this.createNewSession}
            className="new-session-button"
          >
            New Session
          </button>
        </div>
        <div className="messageBox">
          <MessageBox messageContent={currentMessages} />
        </div>
        <Textbox handlerFromParant={this.handleNewUserMessage} />
      </div>
    );
  }
}

export default App;