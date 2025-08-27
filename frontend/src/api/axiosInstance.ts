import axios from "axios";
import {authStore} from "../store/AuthStore.ts";

export const api = axios.create({
    baseURL: "http://127.0.0.1:8000/api"
})

//Подстановка токена
api.interceptors.request.use((config) => {
    if (authStore.accessToken) {
        config.headers.Authorization = `Bearer ${authStore.accessToken}`
    }
    return config
})

//Обработка ошибок
api.interceptors.request.use(
    (response) => response,
    (error) => {
    return Promise.reject(error);
}
)