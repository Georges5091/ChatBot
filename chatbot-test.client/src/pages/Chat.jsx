import React, { useState, useEffect } from 'react';
import ChatService from '../services/ChatService';
import { HiArrowNarrowUp } from 'react-icons/hi'

const Chat = () => {
    const [message, setMessage] = useState('');
    const [messages, setMessages] = useState([]);
    const [current, setCurrent] = useState('');
    const [isSent, setIsSent] = useState(false);

    useEffect(() => {
        if (isSent) {
            displayResponse();
        }
    }, [isSent])

    const sendMessage = (e) => {
        e.preventDefault()
        try {
            let data = { sender: 'Georges', message }
            messages.push(data);
            setMessages(messages);
            setCurrent(message);
            setMessage('');
            setIsSent(true);
            
        } catch (error) {
            console.error('Error sending message: ', error);
        }
    }

    const displayResponse = async () => {
        const response = await ChatService.sendMessage({ message: current });
        console.log(response)

        if (response.data.message === 'Successful') {
            let result = { sender: 'Chat', message: response.data.result }
            messages.push(result)
        }
        setMessages(messages)
        setCurrent('');
        setIsSent(false);
    }

    return (
        <dialog className="messaging-container">
            <div className='messages'>
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.sender === 'Georges' ? 'sent' : 'received'}`}>
                        {msg.message}
                    </div>
                ))}
            </div>
            <form onSubmit={sendMessage} className='message-form'>
                <div className='input-container'>
                    <input type="text"
                        placeholder='Type a message'
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        required
                        className='message-input'
                    />
                    <button type='submit' className={`send ${message.trim().length > 0 ? 'not-empty' : 'empty'}`} disabled={message.trim().length > 0 ? false : true}><HiArrowNarrowUp size={20} color='white' /></button>
                </div>
            </form>
        </dialog>
    );
};

export default Chat;