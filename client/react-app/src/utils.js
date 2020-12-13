
export const getRequestHeaders = (token) => {
    return {
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "applications/json",
        }
    }
}

export const parseJwt = (token) => {
    try {
      return JSON.parse(atob(token.split('.')[1]));
    } catch (e) {
      return null;
    }
  };

///////////////////////////////////////////////////////////

export const treeToTable = (tree) => {
    const depth = getTreeDepth(tree)
    let table = []
    auxTreeToTable(tree.jsonRepr, table, [], depth)
    return [table, depth]
} 

const auxTreeToTable = (node, table, currentRow, maxDepth) => {
    const row = [...currentRow, node.text]
    if (node.children.length == 0){
        // Leaf, lets append a row
        while (row.length < maxDepth){
            row.push("")
        }
        table.push(row)
    } else{
        // Not a leaf, lets call the children
        node.children.forEach(child => {
            auxTreeToTable(
                child, table, row, maxDepth
            )
        })
    }
}

export const tableToGridBlock = (table, depth) => {
    const blocks = []
    let currentText = null
    let newText
    for (let x = 0; x < depth; x++){
        for (let y = 0; y < table.length; y++){
            newText = table[y][x]
            if (newText.length > 0){
                if (y === 0 || newText !== currentText){
                    blocks.push({
                        x: x+1,
                        yStart: y+1,
                        yEnd: y+2,
                        text: newText
                    })
                } else{
                    blocks[-1]["yEnd"] = blocks[-1]["yEnd"] + 1
                }
            }
        }
    }
    return blocks
}

export const getTreeDepth = (tree) => {
    return auxGetTreeDepth(tree.jsonRepr, 0)
}

const auxGetTreeDepth = (node, currentLen) => {
    currentLen++
    if (node.children.length == 0) return currentLen
    else{
        return node.children.reduce((currentmax, child) => {
            return Math.max(
                currentmax,
                auxGetTreeDepth(child, currentLen)
            )
        }, 0)
    }
}