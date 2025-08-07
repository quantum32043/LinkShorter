import Modal from "./Modal.tsx";
import React from "react";
import {observer} from "mobx-react-lite";
import {modalStore} from "../store/ModalStore.ts";

const AuthModal = observer( () => {
    const isLogin = modalStore.mode == "login";
    const hidden = open ? "visible opacity-100" : "invisible opacity-0"
    return(
        <Modal hidden={hidden}>
            <section onClick={e => e.stopPropagation()} className={`w-[25%] h-[75%] bg-[#181E29] border-[#353C4A] rounded-[24px] border-3 ${hidden}`}>
                {/*<button onClick={() => setOpen(false)} className="w-[50px]">×</button>*/}
                <h2 className="text-[60px] pt-[100px] font-sans font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-700 via-pink-500 to-blue-700 text-center">
                    { isLogin ? "Login" : "Registration" }
                    {/*Login*/}
                </h2>
                <form className='p-[20px]'>
                    <input type="email" placeholder="Email"
                           className="w-full mb-8 p-4 border font-sans font-light text-[18px] text-[#C9CED6] pl-[50px] bg-[#181E29] border-[#353C4A] rounded-[48px] border-3"/>
                    <input type="password" placeholder="Password"
                           className="w-full mb-8 p-4 border font-sans font-light text-[18px] text-[#C9CED6] pl-[50px] bg-[#181E29] border-[#353C4A] rounded-[48px] border-3"/>
                    <button type="submit" className="w-full py-2 bg-[#144EE3] text-white rounded-[48px] mb-2">
                        { isLogin ? "Login" : "Registration" }
                        {/*Login*/}
                    </button>
                </form>
                <p className="font-sans text-[18px] text-white text-center">
                    {isLogin ? "No account? " : "Already have an account? "}
                    <button
                        className="underline underline-offset-2 cursor-pointer"
                        onClick={() => modalStore.toggleMode()}
                    >
                        {isLogin ? "Create one" : "Sign In"}
                    </button>
                </p>

            </section>
        </Modal>
    )
})

export default AuthModal;