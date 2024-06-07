import { useState, useEffect } from "react";
import axios from "axios";

function UserInput() {
    const [input, setInput] = useState("");
    const [res, setRes] = useState({});

    const fetchResponse = async () => {
        try {
            const response = await axios.post(
                `https://1c59-108-46-33-124.ngrok-free.app/api/response`, input,
            )
    
            console.log("This is the response data:", response);
            } catch (error) {
                console.error(error);
            }
    };

    function handleChange(event) {
        event.preventDefault();
        console.log(event.target.value)
        setInput(event.target.value);
    };

    async function handleSubmit(event) {
        fetchResponse();
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
            <input 
                type="text"
                value={input}
                onChange={handleChange}
                placeholder="Enter a question"
            />
            <button type="submit" id="submit">
                Enter
            </button>
            </form>
            
        </div>
    );
}

export default UserInput;