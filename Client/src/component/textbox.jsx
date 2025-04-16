import React, { Component } from 'react';
import {Button, FormControl, FormGroup, Glyphicon, InputGroup} from 'react-bootstrap';

class Textbox extends Component{

    constructor(){
        super();
        this.state = {
            messages: [
                {
                    type: 0,
                    text: ""
                }
            ],
            wordcount: 0
        };
    }

    handleChange(e){
        this.setState({
            messages: [
                {
                    type: 0,
                    text: e.target.value
                }
            ],
            wordcount: this.countWords(e.target.value)
        })
        
    };

    countWords(text){
        return text.trim() === "" ? 0 : text.trim().split(/\s+/).length;
      };

    handleClick(evt){
        // console.log("📤 Sending message to parent:", this.state.messages[0].text);
        evt.preventDefault();
        this.props.handlerFromParant(this.state.messages);
        this.setState({
            messages: [
                {
                    type: 0,
                    text: ""
                }
            ],
        });
    };

    keyPress(e){
        // console.log("📤 Sending message to parent:", this.state.messages[0].text);
        if(e.keyCode === 13){
            e.preventDefault();
            this.props.handlerFromParant(this.state.messages);
            this.setState({
                messages: [
                    {
                        type: 0,
                        text: ""
                    }
                ]
            });

        }
    }
    render(){
        return(
            <footer className="navbar-fixed-bottom">
                <div className="text-right text-sm text-gray-500 mt-1">
                          Word Count: {this.state.wordcount}
                            </div>
                <div className="inputBox">
                    <FormGroup>
                        <InputGroup>
                            <FormControl value={this.state.messages[0].text} onChange={this.handleChange.bind(this)}
                                         onKeyDown={this.keyPress.bind(this)} type="text" placeholder="write something...."/>
                            <InputGroup.Button>
                                <Button onClick={this.handleClick.bind(this)} bsStyle="primary"><Glyphicon glyph="glyphicon glyphicon-send"> Send</Glyphicon></Button>
                            </InputGroup.Button>
                        </InputGroup>
                    </FormGroup>
                </div>
            </footer>
        )

    }
}

export default Textbox;
