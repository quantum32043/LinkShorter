import "mobx-react-lite"
import {makeAutoObservable, runInAction} from "mobx";
import {authApi} from "../api/authApi.ts";

class AuthStore {
    isAuthorized = false;
    accessToken: string | null = null
    constructor() {
        makeAutoObservable(this)

        const savedToken = localStorage.getItem("accessToken")
        if (savedToken) {
            this.accessToken = savedToken
            this.isAuthorized = true
        }
    }

    setAuthorized(value) {
        this.isAuthorized = value
    }

    setAccessToken(value) {
        this.accessToken = value
    }

    async login(email: string, password: string) {
        const {data} = await authApi.login(email, password)
        this.accessToken = data.access_token
        this.isAuthorized = true
        localStorage.setItem("accessToken", data.access_token)
        console.log(data)
    }

    async register(email: string, password: string) {
        const {data} = await authApi.register(email, password)
        runInAction(() => {
            this.accessToken = data.accessToken
        })
    }

    async logout() {
        this.accessToken = null
        this.isAuthorized = false
        localStorage.removeItem("accessToken")
    }
}

export const authStore = new AuthStore()
