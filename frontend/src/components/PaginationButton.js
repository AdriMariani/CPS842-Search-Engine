import React from 'react'

const PaginationButton = ({ resultsLength, onClick, text }) => {
    if(resultsLength > 0) {
        return <button onClick={onClick}>{text}</button>
    }
    else {
        return ''
    }
}

export default PaginationButton