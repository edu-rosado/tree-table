import React, { useEffect, useState } from 'react'
import useLocalStorage from '../../hooks/useLocalStorage'
import axios from 'axios'
import { getRequestHeaders, parseJwt, tableToGridBlock, treeToTable } from '../../utils';
import GridBlock from './GridBlock';
import HeaderItem from './HeaderItem';

const current_tt_id = 4;
const token_debug = {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MjIxMzA0MDUyNSwianRpIjoiNmVjZmQ2NGFjMTRlNDVhNTg1ZDU0OWU4MmU0YWM3MjIiLCJ1c2VyX2lkIjoxfQ.CiBVpTgPza8sAGeYckcQzvkKAw7Lhfn6s3vRhRyNob0",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoyMjEzMDQwNTI1LCJqdGkiOiIwNjUxNjc5ZDE1ZTc0OGNhOTBiYTM5NTNhYWZiNWM0MyIsInVzZXJfaWQiOjF9.TFWp50b8A1u9qLOi8jLhn_3lrHX3uqozAD6b7Np-8kM"
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
            const [table, depth] = treeToTable(treeTable)
            setGridBlocks(tableToGridBlock(table, depth))
        }
    }, [treeTable])
    
    return (
        <div className="data-section">
            <div className="grid">
                {treeTable.headers.map((head_text, lv) => (
                    <HeaderItem text={head_text} lv={lv}/>
                ))}
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
        </div>
    )
}
