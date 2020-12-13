import React, { useState } from 'react'
import ActionBar_SimpleButton from './ActionBarSimpleButton'

export default function ActionBar_DropdownButton({
    text, choices
}) {
    const [dropdownIsActive, setDropdownIsActive] = useState(false)
    return (
        <div className="dropdown-container">
            <button 
                className="topbar-btn"
                onMouseEnter={()=>setDropdownIsActive(true)}
                onMouseLeave={()=>setDropdownIsActive(false)}
            >
                {text}
            </button>
            <div
                className={"dropdown-items " + (dropdownIsActive? "active":"")}
                onMouseEnter={()=>setDropdownIsActive(true)}
                onMouseLeave={()=>setDropdownIsActive(false)}
            >
                {choices.map((args, index) => (
                    <ActionBar_SimpleButton
                        key={index}    
                        {...args}/>
                ))}
            </div>
        </div>
    )
}
