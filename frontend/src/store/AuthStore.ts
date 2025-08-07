import "mobx-react-lite"
import {makeAutoObservable} from "mobx";

class AuthStore {
    isAuthorized = false;
    accessToken = ""
    constructor() {
        makeAutoObservable(this)

        const savedToken = localStorage.getItem("accessToken")
        if (savedToken) {
            this.accessToken = savedToken
            this.isAuthorized = true
        }
    }
}

export const authStore = new AuthStore()
