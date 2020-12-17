import React from 'react'

export default function HeaderItem({lv,text}) {
    return (
        <div className="header-item">
            {`Level ${lv}: ${text}`}
        </div>
    )
}
