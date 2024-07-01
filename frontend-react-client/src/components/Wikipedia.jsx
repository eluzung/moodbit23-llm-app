import axios from "axios";
import { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";

function Wikipedia() {
  const navigate = useNavigate();
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(true);
  const [messageList, setMessageList] = useState([]);
  const [state, updateState] = useState();
  const forceUpdate = useCallback(() => updateState({}), []);

  const handleBackButton = () => {
    navigate("/");
  };

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
        `https://794c-108-46-33-124.ngrok-free.app/api/wikipedia`,
        inputObj
      );

      console.log("This is the response: ", response.data.response);
      console.log("This is the response: ", response.data.link);

      msgArr.push({
        role: "Chatbot",
        content: response.data.response,
        link: response.data.link,
      });
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

  function handleMessageList() {
    if (loading === false) {
      forceUpdate();
    }
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
      <div onChange={handleMessageList}>
        {loading ? (
          <p></p>
        ) : (
          <div>
            {messageList.map((message, index) => (
              <div
                key={index}
                className={message.role === "User" ? message.content : ""}
              >
                <span>
                  <b>{message.role}</b>
                </span>
                <span>: </span>
                <span>{message.content}</span>
                <p>
                  <span>
                    Here is the link: <a href={message.link}>{message.link}</a>
                  </span>
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Wikipedia;
