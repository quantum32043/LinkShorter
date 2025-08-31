import {api} from "./axiosInstance.ts";


export const shortApi = {
    short: (original_url: string) => {
        api.post("/short", {original_url: original_url})
    }
}