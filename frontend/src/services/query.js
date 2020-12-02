import axios from 'axios'

const query = async text => {
    const response = await axios.post('http://127.0.0.1:5000/query', { query: text })
    return response.data
}

export default { query }