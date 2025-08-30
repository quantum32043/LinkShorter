import {api} from "./axiosInstance.ts";

export const authApi = {
    login: (username: string, password: string) => {
        const params = new URLSearchParams();
        params.append("username", username)
        params.append("password", password)
        params.append("grant_type", "password")

        return api.post("/login", params, {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
        });
    },
    register: (username: string, password: string) =>
        api.post("/register", { username, password }),
    refresh: () =>
        api.post("/refresh"),
    me: () =>
        api.get("/me")
}