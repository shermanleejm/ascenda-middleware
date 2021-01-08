const { Transaction } = require("../models/Transaction");

exports.getTransactionsByUserId = async (req, res, next) => {
    const { userId } = req.params;

    try {
        const transactions = await Transaction.findAll({
            where: {
                userId: userId,
            },
        });

        if (transactions.length == 0) {
            throw new Error(`Can't find transactions for userId: ${userId}`);
        }

        res.status(200).json({
            transactions,
        });
    } catch (e) {
        if (e.errors) {
            res.status(400).json({
                messages: e.errors.map((error) => error.message),
            });
        } else {
            res.status(400).json({
                message: e || "Failed",
            });
        }
    }
};

exports.updateTransaction = async (req, res, next) => {
    const { amount, transactionCode } = req.body;

    try {
        const [transaction] = await Transaction.findAll({
            where: {
                transactionCode: transactionCode,
            },
        });

        if (!transaction) {
            throw new Error("Can't find transaction");
        }
        transaction.amount = Number.parseFloat(amount);
        await transaction.save();

        res.status(200).json({
            message: "UPDATED!",
            transaction,
        });
    } catch (e) {
        if (e.errors) {
            res.status(400).json({
                messages: e.errors.map((error) => error.message),
            });
        } else {
            res.status(400).json({
                message: e || "Failed",
            });
        }
    }
};

exports.createTransaction = async (req, res, next) => {
    const { userId, memberId, amount, transactionCode } = req.body;
    try {
        const transaction = await Transaction.create({
            transactionCode: transactionCode,
            amount: amount,
            userId: userId,
            memberId: memberId,
        });

        res.status(201).json({
            message: "success",
            transaction,
        });
    } catch (e) {
        if (e.errors) {
            res.status(400).json({
                messages: e.errors.map((error) => error.message),
            });
        } else {
            res.status(400).json({
                message: e || "Failed",
            });
        }
    }
};

exports.getTransaction = async (req, res, next) => {
    const { transactionCode } = req.params;

    try {
        const [transaction] = await Transaction.findAll({
            where: {
                transactionCode: transactionCode,
            },
        });

        if (!transaction) {
            throw new Error("Can't find transaction");
        }

        res.status(200).json({
            transaction,
        });
    } catch (e) {
        if (e.errors) {
            res.status(400).json({
                messages: e.errors.map((error) => error.message),
            });
        } else {
            res.status(400).json({
                message: e,
            });
        }
    }
};
