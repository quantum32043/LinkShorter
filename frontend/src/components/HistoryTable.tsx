const HistoryTable = () => {
    return (
        <table
            className="w-full mt-[140px] mx-[150px] rounded-t-[10px] overflow-hidden font-sans text-[15px] font-bold text-white">
            <tr className="h-[65px] bg-[#181E29]">
                <th>Short Link</th>
                <th>Original Link</th>
                <th>QR Code</th>
                <th>Date</th>
            </tr>
        </table>
    )
}

export default HistoryTable