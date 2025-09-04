import type {HistoryTableRow} from "../types.ts";
import {makeAutoObservable, runInAction} from "mobx";
import {historyApi} from "../api/historyApi.ts";

class HistoryStore {
    history: HistoryTableRow[]

    constructor() {
        makeAutoObservable(this)
    }

    async getHistory() {
        const {data} = await historyApi.getHistory()
        runInAction(() => {
            this.history = data
        })
    }
}