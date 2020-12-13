import { useEffect, useState } from "react";

export default function useLocalStorage(itemKey, initialValue) {
    const localStorageKey = "treetable-" + itemKey
    const [item, setItem] = useState(() => {
        const localValue = JSON.parse(localStorage.getItem(localStorageKey))
        if (localValue === null || localValue === ""){
            return initialValue
        }
        else return localValue
    })

    useEffect(() => {
        localStorage.setItem(
            localStorageKey,
            JSON.stringify(item)
        )
    }, [item])

    return [item, setItem]
    
}
