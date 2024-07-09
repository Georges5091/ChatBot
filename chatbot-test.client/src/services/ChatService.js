import http from '../http-common';

const sendMessage = (data) => {
    return http.post('/chatbot', data);
}

const ChatService = {
    sendMessage,
}

export default ChatService;