import axios from 'axios'

const query = async (query, start, end) => {
    const response = await axios.post('http://127.0.0.1:5000/query', { query, start, end })
    return response.data
}

export default { query }