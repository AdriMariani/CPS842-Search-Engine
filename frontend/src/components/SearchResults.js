import React from 'react'

const SearchResults = ({ results }) => {
    if(results.length > 0) {
        return (
            <ul>
                {
                    results.map(result => {
                        return <li><a key={result.url} href={result.url} target = "_blank" rel = "noopener noreferrer">{result.title}</a></li>
                    })
                }
            </ul>
        )
    } 
    else {
        return <p>No Results Found</p>
    }
}

export default SearchResults