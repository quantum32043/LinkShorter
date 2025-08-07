import {api} from "./axiosInstance.ts";

export const authApi = {
    login: (email: string, password: string) => {
        api.post("/login", { email, password })
    },
    register: (email: string, password: string) => {
        api.post("/register", { email, password })
    },
    logout: () => {
        api.post("/logout")
    },
    refresh: () => {
        api.post("/refresh")
    }
}