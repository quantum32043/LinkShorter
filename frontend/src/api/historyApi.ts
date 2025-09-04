import {api} from "./axiosInstance.ts";

export const historyApi = {
    getHistory: () =>
        api.get("/history")
}