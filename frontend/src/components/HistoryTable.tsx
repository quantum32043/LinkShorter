import React, {useEffect} from "react";
import { observer } from "mobx-react-lite";
import { authStore } from "../store/AuthStore";
import type { HistoryTableRow } from "../types.ts";
import {modalStore} from "../store/ModalStore.ts";

interface HistoryTableProps {
    history: HistoryTableRow[];
}

const HistoryTable: React.FC<HistoryTableProps> = observer(({ history }) => {
    history = [{id: 1,
    shortLink: "string",
    originalLink: "string",
    date: "string"},{id: 1,
        shortLink: "string",
        originalLink: "string",
        date: "string"}, {id: 1,
        shortLink: "string",
        originalLink: "string",
        date: "string"}]
    const showRows = authStore.isAuthorized ? history : history.slice(0, 2);
    return (
        <div className="relative w-full mt-[135px] mx-[150px]">
            <table className="w-full rounded-t-[10px] overflow-hidden font-sans text-[15px] font-bold text-white text-center border-separate border-spacing-y-[3px]">
                <thead>
                <tr className="h-[65px] bg-[#181E29]">
                    <th className="w-1/3">Short Link</th>
                    <th className="w-1/3">Original Link</th>
                    <th className="w-1/3">Date</th>
                </tr>
                </thead>
                <tbody>
                {showRows.length === 0 ? (
                    <tr>
                        <td colSpan={3} className="pt-[20px]">No history yet</td>
                    </tr>
                ) : (
                    showRows.map((row) => (
                        <tr key={row.id} className="h-[65px] bg-[#181E2952] backdrop-blur-lg">
                            <td><a href={row.shortLink}>{row.shortLink}</a></td>
                            <td>{row.originalLink}</td>
                            <td>{row.date}</td>
                        </tr>
                    ))
                )}
                </tbody>
            </table>

            {!authStore.isAuthorized && history.length > 1 && (
                <div
                    className="absolute top-[133px] left-0 right-0 bottom-0 flex items-center justify-center
                     bg-[transperent] backdrop-blur-sm select-none overflow-hidden"
                >
                    <p className="text-white text-xl font-medium">
                        <button className="underline underline-offset-2 cursor-pointer" onClick={() => modalStore.open("login")}>Авторизуйтесь</button>
                        , чтобы увидеть всю историю</p>
                </div>
            )}
        </div>
    );
});

export default HistoryTable;
