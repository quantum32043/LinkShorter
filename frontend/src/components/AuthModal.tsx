import Modal from "./Modal.tsx";
import React, {useState} from "react";
import {observer} from "mobx-react-lite";
import {modalStore} from "../store/ModalStore.ts";
import {authStore} from "../store/AuthStore.ts";

const AuthModal = observer( () => {
    const isLogin = modalStore.mode == "login";
    const hidden = modalStore.isOpen ? "visible opacity-100" : "invisible opacity-0"

    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
            if (isLogin) {
                await authStore.login(username, password)
            } else {
                await authStore.register(username, password)
            }
            modalStore.close() // <-- должно срабатывать, если isOpen реально меняется
        } catch (err) {
            console.error(err) // ловим возможные ошибки из authStore
        }
    }

    return(
        <Modal hidden={hidden}>
            <section onClick={e => e.stopPropagation()} className={`w-[25%] h-[75%] bg-[#181E29] border-[#353C4A] rounded-[24px] border-3 ${hidden}`}>
                {/*<button onClick={() => setOpen(false)} className="w-[50px]">×</button>*/}
                <h2 className="text-[60px] pt-[100px] font-sans font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-700 via-pink-500 to-blue-700 text-center">
                    { isLogin ? "Login" : "Registration" }
                    {/*Login*/}
                </h2>
                <form className='p-[20px]' onSubmit={handleSubmit}>
                    <input type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => (setUsername(e.target.value))}
                        className="w-full mb-8 p-4 border font-sans font-light text-[18px] text-[#C9CED6] pl-[50px] bg-[#181E29] border-[#353C4A] rounded-[48px] border-3"/>
                    <input type="password"
                           placeholder="Password"
                           value={password}
                           onChange={(e) => (setPassword(e.target.value))}
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