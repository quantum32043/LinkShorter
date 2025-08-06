import React from "react";

const Modal = ( {children, modal, setModal, hidden} ) => {
    return(
            <div className={`fixed inset-0 z-50 bg-[#181E2952] backdrop-blur-[3px] flex items-center justify-center ${hidden} transition-all duration-200`}
                onClick={() => setModal(false)}>
                    { children }
            </div>
    )

}


export default Modal;