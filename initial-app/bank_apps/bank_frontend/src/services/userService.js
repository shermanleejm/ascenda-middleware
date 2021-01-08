const url = process.env.REACT_APP_PRODUCTION_ENV_URL

const fetchUser = () => {
    return fetch(url + "/users/1", {
        method: 'GET',
        headers: {
            "Content-Type" : "application/json",
            'x-api-key': process.env.REACT_APP_API_KEY
        }
    })
        .then((res) => res.json())
        .then((result) => {
            return result;
        })
        .catch(e => console.log(e));
};

export default {
    fetchUser
};
