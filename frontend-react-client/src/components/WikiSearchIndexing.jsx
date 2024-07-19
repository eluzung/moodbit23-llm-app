import axios from "axios";
import { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";

function WikiSearchIndexing() {
  const navigate = useNavigate();
  const [input, setInput] = useState("");
  const [result, setResult] = useState("");
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

    // let msgArr = messageList;
    // msgArr.push({ role: "User", content: input });
    // setMessageList(msgArr);

    try {
      let inputObj = {
        strInput: input,
      };

      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/api/load_docs`,
        inputObj
      );

      console.log("This is the response: ", response.data);
      if ((response.data = "success")) {
        const res = await axios.post(
          `${process.env.REACT_APP_API_URL}/api/response_with_indexing`,
          inputObj
        );
        console.log("This is the response: ", res.data);
        // setResult(res);
      }

      //   msgArr.push({
      //     role: "Chatbot",
      //     content: response.data.response,
      //     link: response.data.link,
      //   });
      //   setMessageList(msgArr);
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
      <h1>Wikipedia Search Indexing</h1>
      <button onClick={handleBackButton}>Back</button>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={handleChange}
          placeholder="Enter a question"
          size={50}
        />
        <button type="submit" id="submit">
          Enter
        </button>
      </form>
    </div>
  );
}

export default WikiSearchIndexing;
