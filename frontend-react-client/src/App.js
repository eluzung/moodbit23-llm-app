import { Route, Routes, BrowserRouter } from "react-router-dom";
import "./App.css";
import UserInput from "./components/UserInput";
import Wikipedia from "./components/Wikipedia";
import WebSearch from "./components/WebSearch";

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Routes>
          <Route path="/" element={<UserInput />} />
          <Route path="/wikipedia" element={<Wikipedia />} />
          <Route path="web_search" element={<WebSearch />} />
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
