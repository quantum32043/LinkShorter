import axios from "axios";
import {authStore} from "../store/AuthStore.ts";
import {authApi} from "./authApi.ts";

export const api = axios.create({
    baseURL: "http://127.0.0.1:8000/api",
    withCredentials: true
})

//Подстановка токена
api.interceptors.request.use((config) => {
    if (authStore.accessToken) {
        config.headers.Authorization = `Bearer ${authStore.accessToken}`
        console.log(config + 'req')
    }
    return config
})

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const request = error.config

        if (error.response?.status === 401 && !request._retry) {
            request._retry = true
            try {
                const { data } = await api.post("/refresh")

                localStorage.setItem("accessToken", data.access_token)
                authStore.accessToken = data.access_token

                // обновляем хедер и повторяем запрос
                request.headers.Authorization = `Bearer ${data.access_token}`
                return api(request)
            } catch {
                await authStore.logout()
            }
        }
        return Promise.reject(error)
    }
)