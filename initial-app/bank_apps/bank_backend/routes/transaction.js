const express = require('express')

const transactionController = require('../controllers/transaction')

const router = express.Router();

router.get('/transactions/:userId', transactionController.getTransactionsByUserId)

router.get('/transaction/:transactionCode', transactionController.getTransaction)

router.post('/transaction', transactionController.createTransaction)

router.put('/transaction', transactionController.updateTransaction)

module.exports = router;