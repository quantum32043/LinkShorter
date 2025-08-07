import React from "react";
import {modalStore} from "../store/ModalStore.ts";

const Modal = ( {children, hidden} ) => {
    return(
            <div className={`fixed inset-0 z-50 bg-[#181E2952] backdrop-blur-[3px] flex items-center justify-center ${hidden} transition-all duration-200`}
                onClick={() => modalStore.close()}>
                    { children }
            </div>
    )

}


export default Modal;