import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

function JSONValidator() {
  const navigate = useNavigate();
  const [input, setInput] = useState("");
  const [fixInput, setFixInput] = useState("");
  const [res, setRes] = useState("");
  const [fixRes, setFixRes] = useState("");
  const [loading, setLoading] = useState(true);

  const handleBackButton = () => {
    navigate("/");
  };

  const fetchResponse = async () => {
    setLoading(true);

    if (!input) return;

    try {
      let inputObj = {
        strInput: input,
      };

      const response = await axios.post(
        `https://794c-108-46-33-124.ngrok-free.app/api/json`,
        inputObj
      );

      console.log("This is the response: ", response.data);
      const response_string = JSON.stringify(response.data);
      console.log("This is the new response: ", response_string);

      setRes(response_string);

      setLoading(false);
      setInput("");
    } catch (error) {
      console.error(error);
    }
  };

  const fetchFixResponse = async () => {
    setLoading(true);

    if (!fixInput) return;

    try {
      let inputObj = {
        strInput: fixInput,
      };

      const response = await axios.post(
        `https://794c-108-46-33-124.ngrok-free.app/api/fix_json`,
        inputObj
      );

      console.log("This is the response: ", response.data);
      const response_string = JSON.stringify(response.data);
      console.log("This is the new response: ", response_string);

      setRes(response_string);

      setLoading(false);
      setInput("");
    } catch (error) {
      console.error(error);
    }
  };

  function handleChange(event) {
    setInput(event.target.value);
  }

  function handleFixChange(event) {
    setFixInput(event.target.value);
  }

  function handleSubmit(event) {
    event.preventDefault();
    fetchResponse();
  }

  function handleFixSubmit(event) {
    event.preventDefault();
    fetchFixResponse();
  }

  return (
    <div>
      <h1>JSON Validator</h1>
      <button id="back-button" onClick={handleBackButton}>
        Back
      </button>
      <form onSubmit={handleSubmit}>
        <p>
          <label>Enter a prompt that will answer as a JSON object!</label>
        </p>
        <textarea value={input} onChange={handleChange} rows="6" cols="50" />
        <button type="submit" id="submit">
          Enter
        </button>
      </form>
      <div>
        {loading ? (
          <p></p>
        ) : (
          <div>
            <p>{res}</p>
          </div>
        )}
      </div>
      <div>
        <form onSubmit={handleFixSubmit}>
          <p>
            <label>Enter an invalid JSON object to validate!</label>
          </p>
          <textarea
            value={fixInput}
            onChange={handleFixChange}
            rows="10"
            cols="50"
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
              <p>{fixRes}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default JSONValidator;
