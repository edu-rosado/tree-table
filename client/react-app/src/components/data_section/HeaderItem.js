import React, { useEffect, useRef, useState } from 'react'

export default function HeaderItem({lv, text, setColumnsWidth}) {

    const [initialX, setInitialX] = useState(0)
    const [currentX, setCurrentX] = useState(0)
    const [headerText, setHeaderText] = useState(`Level ${lv}: ${text}`)

    const resizeUpdate = useRef( 
        (e) => setCurrentX(e.pageX)
    )

    const handleResizeStart = (e) => {
        setInitialX(e.pageX)
        document.addEventListener("mousemove",resizeUpdate.current, false)
    }

    useEffect(() => {
        setColumnsWidth(prev => ([
            ...prev.slice(0,lv),
            prev[lv] + (currentX - initialX) / 28,
            ...prev.slice(lv+1),
        ]))
        setInitialX(currentX)
    }, [currentX])

    useEffect(() => {
        document.addEventListener("mouseup",()=>{
            document.removeEventListener("mousemove",resizeUpdate.current, false)
        })
    }, [])


    return (
        <div className="header-item">
            <h3>{headerText}</h3>
            <div 
                className="resize-element"
                onMouseDown={handleResizeStart}
            ></div>
        </div>
    )
}
