import { useState, useCallback } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function UserInput() {
  const navigate = useNavigate();
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(true);
  const [messageList, setMessageList] = useState([]);
  const [state, updateState] = useState();
  const forceUpdate = useCallback(() => updateState({}), []);

  const handleWikiPage = () => {
    navigate("/wikipedia");
  };

  const handleWebSearchPage = () => {
    navigate("/web_search")
  }

  const fetchResponse = async () => {
    setLoading(true);

    if (!input) return;

    let msgArr = messageList;
    msgArr.push({ role: "User", content: input });
    setMessageList(msgArr);

    try {
      let inputObj = {
        strInput: input,
      };

      const response = await axios.post(
        `https://7451-108-46-33-124.ngrok-free.app/api/response`,
        inputObj
      );

      msgArr.push({ role: "Chatbot", content: response.data });
      setMessageList(msgArr);
      setLoading(false);
      setInput("");
    } catch (error) {
      console.error(error);
    }
  };

  function handleChange(event) {
    setInput(event.target.value);
  }

  function handleSubmit(event) {
    event.preventDefault();
    fetchResponse();
    console.log(messageList);
  }

  function handleMessageList() {
    if (loading === false) {
      forceUpdate();
    }
  }

  return (
    <div>
      <h1>Welcome to chatting with ChatBot!</h1>
      <button id="wiki-button" onClick={handleWikiPage}>
        Search the Wiki through chat!
      </button>
      <button id="web-search-button" onClick={handleWebSearchPage}>
        Search the Web!
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
      <div onChange={handleMessageList}>
        {loading ? (
          <p></p>
        ) : (
          <div>
            {messageList.map((message, index) => (
              <p
                key={index}
                className={message.role === "User" ? message.content : ""}
              >
                <span>
                  <b>{message.role}</b>
                </span>
                <span>: </span>
                <span>{message.content}</span>
              </p>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default UserInput;
