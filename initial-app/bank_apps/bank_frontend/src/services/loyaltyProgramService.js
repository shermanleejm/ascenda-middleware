const url = process.env.REACT_APP_PRODUCTION_ENV_URL

const fetchLoyaltyPrograms = () => {
    return fetch(url + "/loyaltyprograms", {
        headers: {
            "Content-Type" : "application/json",
            'x-api-key': process.env.REACT_APP_API_KEY
        }
    })
        .then((res) => res.json())
        .then((result) => {
            return result;
        })
        .catch(console.log);
};

const validateMembership = async (userData) => {
    const response = await fetch(url + "/validatemembership", {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'x-api-key': process.env.REACT_APP_API_KEY
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(userData)
    })
    if(response.ok){
        return response.json()
    }
    return false
}

const submitAccrualRequest = async (accrualData) => {
    const response = await fetch(url + "/newaccrual", {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'x-api-key': process.env.REACT_APP_API_KEY
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(accrualData)
    })
    if(response.ok){
        return response.json()
    }
    return false
}

const pollAccrualResult = (transactionId) => {
    return fetch(url + "/transaction/status/" + transactionId, {
        headers: {
            "Content-Type" : "application/json",
            'x-api-key': process.env.REACT_APP_API_KEY
        }
    })
        .then((res) => res.json())
        .then((result) => {
            return result;
        })
        .catch(console.log);
};

export default {
    fetchLoyaltyPrograms,
    validateMembership,
    submitAccrualRequest,
    pollAccrualResult
};
