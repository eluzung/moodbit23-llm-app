import './App.css';
import UserInput from './components/UserInput';
import Wikipedia from './components/Wikipedia';

function App() {
  return (
    <div className="App">
      <h1>Welcome to chatting with ChatBot!</h1>
      <UserInput/>
      <h1>Search through Wikipedia!</h1>
      <Wikipedia/>
    </div>
  );
}

export default App;
