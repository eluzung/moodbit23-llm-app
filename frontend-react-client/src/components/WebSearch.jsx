import axios from "axios";
import { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";

function WebSearch() {
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
        `${process.env.REACT_APP_API_URL}/api/web_scraping_search`,
        inputObj
      );

      if (response.data.summary_list) {
        msgArr.push({ role: "Chatbot", content: response.data.summary_list });
      } else {
        msgArr.push({
          role: "Chatbot",
          content: response.data.answer,
          sources: response.data.sources,
        });
      }

      console.log("this is the message array: ", msgArr);
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
      <h1>Search The Web!</h1>
      <button id="back-button" onClick={handleBackButton}>
        Back
      </button>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={handleChange}
          placeholder="Ask me anything"
          size={50}
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
                {Array.isArray(message.content) ? (
                  <div>
                    <span>Here are some results:</span>
                    {message.content.map((item, i) => (
                      <ul key={i}>
                        <li>{item.title}</li>
                        <li>{item.summary}</li>
                        <li>
                          <a href={item.source}>{item.source}</a>
                        </li>
                      </ul>
                    ))}
                  </div>
                ) : (
                  <div>
                    <span>{message.content}</span>
                    <p>
                      <span>
                        <a href={message.sources}>{message.sources}</a>
                      </span>
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default WebSearch;
