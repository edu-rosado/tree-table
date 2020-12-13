import React, { useState } from 'react'
import ActionBar_DropdownButton from './ActionBarDropdownButton'
import ActionBar_SimpleButton from './ActionBarSimpleButton'

const FILE_BTN_CHOICES = [
    {
        text: "Save",
        link: "",
    },
    {
        text: "Delete",
        link: "",
    },
]

export default function ActionBar() {
    return (
        <div className="action-bar">
            <ActionBar_DropdownButton 
                text="File"
                choices={FILE_BTN_CHOICES}
            />
            <ActionBar_SimpleButton 
                text="All you T-Ts"
                link=""
            />
            <ActionBar_SimpleButton 
                text="Discover new T-Ts"
                link=""
            />
        </div>
    )
}
