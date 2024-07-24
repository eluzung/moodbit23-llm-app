import { Route, Routes, BrowserRouter } from "react-router-dom";
import "./App.css";
import UserInput from "./components/UserInput";
import Wikipedia from "./components/Wikipedia";
import WebSearch from "./components/WebSearch";
import JSONValidator from "./components/JSONValidator";
import Indexing from "./components/Indexing";

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Routes>
          <Route path="/" element={<UserInput />} />
          <Route path="/wikipedia" element={<Wikipedia />} />
          <Route path="web_search" element={<WebSearch />} />
          <Route path="/json_validator" element={<JSONValidator />} />
          <Route path="/indexing" element={<Indexing />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;

{
  /* <h1>Welcome to chatting with ChatBot!</h1>
<UserInput/>
<h1>Search through Wikipedia!</h1>
<Wikipedia/> */
}
