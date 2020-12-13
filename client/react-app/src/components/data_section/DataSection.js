import React, { useEffect, useState } from 'react'
import useLocalStorage from '../../hooks/useLocalStorage'
import axios from 'axios'
import { getRequestHeaders, parseJwt, tableToGridBlock, treeToTable } from '../../utils';
import GridBlock from './GridBlock';

const current_tt_id = 2;
const token_debug = {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MjIxMjY3MjQzMSwianRpIjoiNWY1ZTBiMDI2ZTJmNDg2NTlhYzc3OGVmZDQzZmY1NDkiLCJ1c2VyX2lkIjoxfQ.bG-fIRQVwhvny3WahGD_4oMSEaSimBzAGOWZnXVzuUE",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoyMjEyNjcyNDMxLCJqdGkiOiJjMWQ3NDhjMjRkMGM0YWIwODM5NGQ3NWJmYjNlY2Y0MyIsInVzZXJfaWQiOjF9.VGk87aS9_xErG6h7kA3q7rX062IzH12pmu2W1nIUleY"
}

export default function DataSection() {

    const [gridBlocks, setGridBlocks] = useState([])
    
    const [treeTable, setTreeTable] = useLocalStorage("treeTable", null)
    const [tokens, setTokens] = useLocalStorage("tokens", token_debug)

    // TOKENS
    useEffect(() => {
        if (tokens === null){
            // TODO: re-login
        } else{
            const now = new Date()
            const accessDate = new Date(parseJwt(tokens.access).exp)
            if (accessDate <= now){
                const refreshDate = new Date(parseJwt(tokens.refresh).exp)
                if (refreshDate <= now){
                    // TODO: re-login
                } else{
                    let body = {refresh: tokens.refresh}
                    axios.post(
                        "/api/token/refresh/",
                        body,
                        {headers:{"Content-Type": "application/json"}}
                    ).then(res => {
                        setTokens({...res.data, body})
                    }).catch(err => {console.log(err.response)})
                }
            }
        }
    }, [tokens])
    
    // GET DATA
    useEffect(() => {
        if (treeTable === null || treeTable.id !== current_tt_id){
            axios.get(
                `/api/treetables/${current_tt_id}/`,
                getRequestHeaders(tokens.access)
                
            ).then(res => {
                setTreeTable(res.data)
            }).catch(err => {
                console.log(err.response)
                // TODO: re-login?
            })
        } else{
            setGridBlocks(tableToGridBlock(...treeToTable(treeTable)))
        }
    }, [treeTable])
    
    return (
        <div className="data-section">
            {gridBlocks.length === 0 ? "" : (
                gridBlocks.map((data,index) => (
                    <GridBlock
                        key={index} 
                        x={data.x}
                        yStart={data.yStart}
                        yEnd={data.yEnd}
                        text={data.text}/>
                ))
            )}
        </div>
    )
}
