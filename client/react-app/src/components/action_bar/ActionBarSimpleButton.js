import React from 'react'

export default function ActionBar_SimpleButton({
    text, link
}) {
    return (
        <button className="topbar-btn">
            {text}
        </button>
    )
}
