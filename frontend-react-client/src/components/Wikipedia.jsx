import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Wikipedia() {
  const navigate = useNavigate();
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(true);
  const [messageList, setMessageList] = useState([]);

  const handleBackButton = () => {
    navigate("/");
  };

  const fetchResponse = async () => {
    setLoading(true);

    if (!input) return;

    let msgArr = messageList;
    msgArr.push({ author: "User", message: input });
    setMessageList(msgArr);

    try {
      let inputObj = {
        strInput: input,
      };

      const response = await axios.post(
        `https://7249-108-46-33-124.ngrok-free.app/api/wikipedia`,
        inputObj
      );

      msgArr.push({ author: "Chatbot", message: response.data.output });
      setMessageList(msgArr);
      setLoading(false);
      setInput("");
    } catch (error) {
      console.error(error);
    }
  };

  function handleChange(event) {
    event.preventDefault();
    setInput(event.target.value);
  }

  function handleSubmit(event) {
    event.preventDefault();
    fetchResponse();
  }

  return (
    <div>
      <h1>Search through Wikipedia!</h1>
      <button id="back-button" onClick={handleBackButton}>
        Back
      </button>
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
      <div>
        {loading ? (
          <p></p>
        ) : (
          <div>
            {messageList.map((message, index) => (
              <p
                key={index}
                className={message.author === "User" ? message.message : ""}
              >
                <span>
                  <b>{message.author}</b>
                </span>
                <span>: </span>
                <span>{message.message}</span>
              </p>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Wikipedia;
