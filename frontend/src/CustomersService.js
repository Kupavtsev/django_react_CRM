import axios from 'axios';


const instance = axios.create({
    // withCredentials: true,
    baseURL: 'http://localhost:8000',
    headers: {
        "Authorization": "Token 7cae7e36d9acccd313dc00fb429d27584b35dae0"
    }
});


const API_URL = 'http://localhost:8000';

export default class CustomersService{

    constructor(){}


    getCustomers() {
        return instance
            .get('/api/customers/')
            .then(response => response.data);
    }
    // getCustomers() {
    //     const url = `${API_URL}/api/customers/`;
    //     return axios.get(url).then(response => response.data);
    // }
    getCustomersByURL(link){
        const url = `${API_URL}${link}`;
        return axios.get(url).then(response => response.data);
    }
    getCustomer(pk) {
        const url = `${API_URL}/api/customers/${pk}`;
        return axios.get(url).then(response => response.data);
    }
    deleteCustomer(customer){
        const url = `${API_URL}/api/customers/${customer.pk}`;
        return axios.delete(url);
    }
    createCustomer(customer){
        return instance
            .post('/api/customers/',customer);
    }
    // createCustomer(customer){
    //     const url = `${API_URL}/api/customers/`;
    //     return axios.post(url,customer);
    // }
    updateCustomer(customer){
        const url = `${API_URL}/api/customers/${customer.pk}`;
        return axios.put(url,customer);
    }
}