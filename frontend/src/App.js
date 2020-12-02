import queryService from './services/query'
import { useState } from 'react'
import SearchResults from './components/SearchResults'

const App = () => {
  const [searchText, setSearchText] = useState('')
  const [searchResults, setResults] = useState([])
  const [searched, setSearched] = useState(false)

  const search = async () => {
    const results = await queryService.query(searchText)
    setResults(results)
    setSearched(true)
  }

  return (
    <div>
      <h3>CPS 842 - A3</h3>
      <input type="text" value={searchText} onChange={event => setSearchText(event.target.value)}/>
      <button onClick={search}>Search</button>
      <div>
        { searched 
            ? <><p>Found {searchResults.length} results</p><SearchResults results={searchResults}/></>
            : '' 
        }
      </div>
    </div>
  )
}

export default App;
