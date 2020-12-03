import queryService from './services/query'
import { useState } from 'react'
import SearchResults from './components/SearchResults'
import PaginationButton from './components/PaginationButton'

const App = () => {
  const pageLength = 25

  const [searchText, setSearchText] = useState('')
  const [queryField, setQueryField] = useState('')
  const [searchResults, setResults] = useState([])
  const [prevSearchResults, setPrevResults] = useState([])
  const [nextSearchResults, setNextResults] = useState([])
  const [searched, setSearched] = useState(false)
  const [start, setStart] = useState(0)
  const [end, setEnd] = useState(pageLength)

  const search = async e => {
    e.preventDefault()
    const newStart = 0
    const newEnd = pageLength
    const results = await queryService.query(queryField, newStart, newEnd)
    const nextResults = await queryService.query(queryField, newStart + pageLength, newEnd + pageLength)
    setNextResults(nextResults)
    setResults(results)
    setPrevResults([])
    setSearchText(queryField)
    setSearched(true)
    setStart(newStart)
    setEnd(newEnd)
  }

  const next = async e => {
    e.preventDefault()
    const newStart = start + pageLength
    const newEnd = end + pageLength
    const nextResults = await queryService.query(searchText, newStart + pageLength, newEnd + pageLength)
    setPrevResults(searchResults)
    setResults(nextSearchResults)
    setNextResults(nextResults)
    setStart(newStart)
    setEnd(newEnd)
  }

  const previous = async e => {
    e.preventDefault()
    const newStart = start - pageLength
    const newEnd = end - pageLength
    const prevResults = await queryService.query(searchText, newStart - pageLength, newEnd - pageLength)
    setNextResults(searchResults)
    setResults(prevSearchResults)
    setPrevResults(prevResults)
    setStart(newStart)
    setEnd(newEnd)
  }

  return (
    <div>
      <h3>CPS 842 - A3</h3>
      <input type="text" value={queryField} onChange={event => setQueryField(event.target.value)}/>
      <button onClick={search}>Search</button>
      <br/><br/>
      <div>
        { searched 
            ? <>
                <PaginationButton resultsLength={prevSearchResults.length} onClick={previous} text='Previous'/>
                <PaginationButton resultsLength={nextSearchResults.length} onClick={next} text='Next'/>
                <SearchResults
                  results={searchResults} 
                />
              </>
            : '' 
        }
      </div>
    </div>
  )
}

export default App;
