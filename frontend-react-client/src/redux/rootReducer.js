import { combineReducers } from "redux";
import openaiReducer from "./openai/openai.reducer";

const rootReducer = combineReducers({
    openai: openaiReducer,
});

export default rootReducer;