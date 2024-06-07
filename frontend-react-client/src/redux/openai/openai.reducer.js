import openaiActionTypes from "./openai.type";

export const initialState = {
    response: {},
    chatHistory: [],
};

const openaiReducer = (state=initialState, action) => {
    console.log("This is in the openaiReducer:", action);

    switch(action.type) {
        case openaiActionTypes.get_response:
            return {...state, response: action.payload};
        case openaiActionTypes.get_history:
            return {...state, chatHistory: action.payload};
        case openaiActionTypes.delete_history:
            return {...state, chatHistory: {}};
        default:
            return state;
    }
};

export default openaiReducer;