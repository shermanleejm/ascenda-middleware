const { Sequelize, DataTypes } = require("sequelize");
const sequelize = new Sequelize({
    dialect: "sqlite",
    storage: "./db/bankdb.sqlite3",
});

const Transaction = sequelize.define(
    "Transaction",
    {
        // Model attributes are defined here
        transactionCode: {
            type: DataTypes.STRING,
            unique: true,
            allowNull: false,
        },
        memberId: {
            type: DataTypes.STRING,
        },
        userId: {
            type: DataTypes.STRING,
        },
        outcomeCode: {
            type: DataTypes.STRING,
            defaultValue: "PENDING",
        },
        amount: {
            type: DataTypes.FLOAT,
        },
    },
    {}
);

exports.Transaction = Transaction;
