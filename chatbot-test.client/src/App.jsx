import { useState } from 'react';
import './App.css';
import Chat from './pages/Chat';
import { LuMessagesSquare } from 'react-icons/lu'

function App() {
    const [isOpen, setIsOpen] = useState(false)

    const openChat = () => {
        setIsOpen(!isOpen)
    }
    return (
        <>
            <button onClick={openChat} className='open'><LuMessagesSquare color='white' size={25} /></button>
            {isOpen && <Chat />}
        </>
    );
}

export default App;