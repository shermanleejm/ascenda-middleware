const url = process.env.REACT_APP_DEV_ENV_BANK_URL

const fetchTransactions = () => {
    return fetch(url + "/transactions/1")
        .then((res) => res.json())
        .then((result) => {
            return result.transactions;
        })
        .catch(e => console.log(e));
};

const fetchTransactionDetails = (transactionId) => {
    return fetch(url + "/transactions/" + transactionId)
        .then((res) => res.json())
        .then((result) => {
            return result;
        })
        .catch(e => console.log(e));
};

const addTransaction = async (transactionData) => {
    //body -> { userId, memberId, amount, transactionCode }
    const response = await fetch(url + "/transaction", {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(transactionData)
    })
    if(response.ok){
        return response.json()
    }
    return false
}

export default {
    fetchTransactions,
    fetchTransactionDetails,
    addTransaction
};