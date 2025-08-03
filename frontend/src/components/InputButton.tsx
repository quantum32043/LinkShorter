const handleClick = () => {

}

const InputButton = () => {
    return (
        <div className="relative w-[660px] h-[76px] mt-[45px]">
            <input placeholder="Enter the link here"
                   className="w-[660px] h-[76px] font-sans font-light text-[18px] text-[#C9CED6] pl-[70px] bg-[#181E29] border-[#353C4A] rounded-[48px] border-3"/>
            <button
                className="absolute inset-y-0 right-0 w-[178px] h-[60px] bg-[#144EE3] rounded-[48px] text-white font-semibold font-sans text-[16px] m-[8px]"
                onClick={handleClick}>
                Shorten Now!
            </button>
        </div>
    )
}

export default InputButton