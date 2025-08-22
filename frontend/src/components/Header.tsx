import React, {useState} from "react";
import {observer} from "mobx-react-lite";
import {modalStore} from "../store/ModalStore.ts";
import {authApi} from "../api/authApi.ts";
import {authStore} from "../store/AuthStore.ts";

const Header = observer(() => {
    return(
        <>
            <header className="z-50 w-full h-auto px-[47px] py-[40px] bg-transparent fixed">
                <div className="h-[60px] flex flex-row items-center justify-between">
                    <a href={"#"}
                       className="text-transparent text-[37px] font-sans font-bold bg-clip-text bg-gradient-to-r from-blue-700 via-pink-500 to-blue-700">Shorter</a>
                    {!authStore.isAuthorized ? (
                    <div className="w-[322px] h-full flex justify-between items-center">
                        <button
                            type={"button"}
                            onClick={() => {
                                modalStore.open("login")
                            }}
                            className="w-[125px] h-full border-[#353C4A] border-1 rounded-[48px] bg-[#181E29] font-bold font-sans text-white text-[16px]">
                            Login
                        </button>
                        <button
                            type={"button"}
                            onClick={() => {
                                modalStore.open("register")
                            }}
                            className="w-[180px] h-full border-[#144EE3] border-1 rounded-[48px] bg-[#144EE3] font-bold font-sans text-white text-[16px]">
                            Register Now
                        </button>
                    </div>
                    ) : (
                        <button
                            type={"button"}
                            onClick={async () => {
                                try {
                                    await authStore.logout()
                                } catch (e) {
                                    console.error(e)
                                }
                            }}
                            className="w-[180px] h-full border-[#144EE3] border-1 rounded-[48px] bg-[#144EE3] font-bold font-sans text-white text-[16px]">
                            Logout
                        </button>
                    )}
                </div>
            </header>
        </>
    )
})

export default Header