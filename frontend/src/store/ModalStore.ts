import {makeAutoObservable} from "mobx";

class ModalStore {
    isOpen = false;
    mode: "login" | "register" | null = null;

    constructor() {
        makeAutoObservable(this)
    }

    open(mode: "login" | "register") {
        this.isOpen = true
        this.mode = mode
    }

    close() {
        this.isOpen = false
        this.mode = null
    }

    toggleMode() {
        this.mode = this.mode == "login" ? "register" : "login"
    }
}

export const modalStore = new ModalStore();