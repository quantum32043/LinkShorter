import React from "react";
import type {HistoryTableRow} from "../types.ts";


interface HistoryTableProps {
    history: HistoryTableRow[]
}

const HistoryTable: React.FC<HistoryTableProps> = ({ history }) => (
        <table
            className="w-full mt-[140px] mx-[150px] rounded-t-[10px] overflow-hidden font-sans text-[15px] font-bold text-white text-center border-separate border-spacing-y-[3px]">
            <thead>
                <tr className="h-[65px] bg-[#181E29]">
                    <th className="w-1/3">Short Link</th>
                    <th className="w-1/3">Original Link</th>
                    <th className="w-1/3">Date</th>
                </tr>
            </thead>
            <tbody>
                {history.length == 0 ? (
                    <tr>
                        <td colSpan={3} className="pt-[20px] t">
                            No history yet
                        </td>
                    </tr>
                ) : (
                    history.map(row => (
                    <tr key={row.id} className="h-[65px] bg-[#181E2952] backdrop-blur-lg">
                        <td>
                            <a href={row.shortLink}>{row.shortLink}</a>
                        </td>
                        <td>
                            {row.originalLink}
                        </td>
                        <td>{row.date}</td>
                    </tr>
                )))}
            </tbody>
        </table>
    );

export default HistoryTable