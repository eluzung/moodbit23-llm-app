import axios from "axios";
import openaiActionTypes from "./openai.type";

export const getResponse = (payload) => ({
    type: openaiActionTypes.get_response,
    payload: payload,
});

export const getHistory = (payload) => ({
    type: openaiActionTypes.get_history,
    payload: payload,
});

export const deleteHistory = () => ({
    type: openaiActionTypes.delete_history,
});

export const getResponseThunk = (userInput) => {
    return async (dispatch) => {
        try {
            const response = await axios.post(
                `https://f7e2-108-46-33-124.ngrok-free.app/api/response`, userInput,
            )

            console.log("This is the response data:", response.data);
            dispatch(getResponse(response.data));
        } catch (error) {
            console.error(error);
        }
    }
};

export const getHistoryThunk = () => {
    return async (dispatch) => {
        try {
            const response = await axios.post(
                `https://f7e2-108-46-33-124.ngrok-free.app/api/chathistory`
            )

            console.log("This is the response HISTORY data:", response.data);
            dispatch(getHistory(response.data));
        } catch (error) {
            console.error(error);
        }
    }
};

export const deleteHistoryThunk = () => {
    return async (dispatch) => {
        try {
            const response = await axios.delete(
                `https://f7e2-108-46-33-124.ngrok-free.app/api/chathistory`
            )

            console.log("This is the delete history response:", response);
            dispatch(getHistory(response));
        } catch (error) {
            console.error(error);
        }
    }
};