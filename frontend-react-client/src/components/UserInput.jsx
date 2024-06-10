import { useState, useEffect } from "react";
import axios from "axios";

function UserInput() {
    const [input, setInput] = useState("");
    const [res, setRes] = useState({});

    const fetchResponse = async () => {
        try {
            let inputObj = {
                strInput: input
            };
            console.log(inputObj);
            
            const response = await axios.post(`https://a92d-108-46-33-124.ngrok-free.app/api/response`, inputObj);
    
            console.log("This is the response data:", response.data);
            } catch (error) {
                console.error(error);
            }
    };

    function handleChange(event) {
        event.preventDefault();
        setInput(event.target.value);
    };

    async function handleSubmit(event) {
        event.preventDefault()
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