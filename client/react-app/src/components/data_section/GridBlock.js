import React from 'react'

export default function GridBlock({x, yStart, yEnd, text}) {

    const styles = {
        gridColumnStart: x,
        gridColumnEnd: x+1,
        gridRowStart: yStart,
        gridRowEnd: yEnd,
    }
    return (
        <div
            className="grid-block"
            style={styles}>
            <p>{text}</p>
        </div>
    )
}
