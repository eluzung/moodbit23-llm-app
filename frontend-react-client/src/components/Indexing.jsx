import axios from "axios";
import { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";

function Indexing() {
  const navigate = useNavigate();
  const [input, setInput] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(true);
  const [messageList, setMessageList] = useState([]);
  const [state, updateState] = useState();
  const forceUpdate = useCallback(() => updateState({}), []);

  const handleBackButton = () => {
    navigate("/");
  };

  const uploadFile = async () => {
    const formData = new FormData();

    console.log("this is the file: ", selectedFile);
    console.log("this is the file path: ", selectedFile.path);

    formData.append("file", selectedFile);

    console.log("this is the form data: ", formData);
    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/api/file_upload`,
        formData
      );
      console.log("This is the response: ", response.data);
    } catch (error) {
      console.error(error);
    }
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
        `${process.env.REACT_APP_API_URL}/api/indexing/response`,
        inputObj
      );

      console.log("This is the response: ", response.data.response);

        msgArr.push({
          role: "Chatbot",
          content: response.data.response,
        });
      setMessageList(msgArr);
      setLoading(false);
      setInput("");
    } catch (error) {
      console.error(error);
    }
  };

  //   const fetchResponse = async () => {
  //     setLoading(true);

  //     if (!input) return;

  //     // let msgArr = messageList;
  //     // msgArr.push({ role: "User", content: input });
  //     // setMessageList(msgArr);

  //     try {
  //       let inputObj = {
  //         strInput: input,
  //       };

  //       const response = await axios.post(
  //         `${process.env.REACT_APP_API_URL}/api/load_docs`,
  //         inputObj
  //       );

  //       console.log("This is the response: ", response.data);
  //       if ((response.data = "success")) {
  //         const res = await axios.post(
  //           `${process.env.REACT_APP_API_URL}/api/response_with_indexing`,
  //           inputObj
  //         );
  //         console.log("This is the response: ", res.data);
  //         // setResult(res);
  //       }

  //       //   msgArr.push({
  //       //     role: "Chatbot",
  //       //     content: response.data.response,
  //       //     link: response.data.link,
  //       //   });
  //       //   setMessageList(msgArr);
  //       setLoading(false);
  //       setInput("");
  //     } catch (error) {
  //       console.error(error);
  //     }
  //   };

  function handleFileChange(event) {
    event.preventDefault();
    console.log("this is the file event: ", event.target.files);
    setSelectedFile(event.target.files[0]);
  }

  function handleFileSubmit(event) {
    event.preventDefault();
    uploadFile();
  }

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
      <h1>Index through documents and search!</h1>
      <button onClick={handleBackButton}>Back</button>
      <form onSubmit={handleFileSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
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
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Indexing;
